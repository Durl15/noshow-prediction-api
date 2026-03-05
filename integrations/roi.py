from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/roi", tags=["roi-calculator"])

class Metrics(BaseModel):
    total_appointments_monthly: int
    no_show_count_monthly: int
    avg_revenue_per_visit: float = 150.0
    staff_cost_per_hour: float = 50.0
    prediction_accuracy: float = 0.85

@router.post("/calculate")
async def calc_roi(m: Metrics):
    rate = m.no_show_count_monthly / m.total_appointments_monthly if m.total_appointments_monthly > 0 else 0
    monthly_lost = m.no_show_count_monthly * m.avg_revenue_per_visit
    monthly_staff = m.no_show_count_monthly * 30 * (m.staff_cost_per_hour / 60)
    monthly_opp = monthly_lost * 0.3
    total_monthly = monthly_lost + monthly_staff + monthly_opp
    
    reduction = 0.25 + (m.prediction_accuracy - 0.8) * 0.5
    reduction = max(0.15, min(0.50, reduction))
    prevented = m.no_show_count_monthly * reduction
    monthly_savings = prevented * (m.avg_revenue_per_visit * 0.8)
    
    intervention = int(m.total_appointments_monthly * 0.3) * 3.50
    system_cost = 500
    net_monthly = monthly_savings - intervention - system_cost
    
    roi = ((net_monthly) / (intervention + system_cost)) * 100 if (intervention + system_cost) > 0 else 0
    be = system_cost / (monthly_savings - intervention) if (monthly_savings - intervention) > 0 else 999
    
    return {
        "current_monthly_no_show_cost": round(total_monthly, 2),
        "current_annual_no_show_cost": round(total_monthly * 12, 2),
        "no_show_rate_percent": round(rate * 100, 2),
        "potential_savings_monthly": round(monthly_savings, 2),
        "net_annual_benefit": round(net_monthly * 12, 2),
        "roi_percent": round(roi, 2),
        "break_even_months": round(be, 1)
    }

@router.get("/scenarios")
async def scenarios(appointments: int = 1000, no_show_rate: float = 0.15, revenue: float = 150.0):
    results = []
    for reduction_pct in [15, 25, 35, 50]:
        reduction = reduction_pct / 100
        current_no_shows = int(appointments * no_show_rate)
        prevented = current_no_shows * reduction
        annual_savings = prevented * revenue * 12
        annual_costs = (appointments * 0.3 * 3.50 * 12) + (500 * 12)
        net = annual_savings - annual_costs
        roi = (net / annual_costs) * 100 if annual_costs > 0 else 0
        results.append({
            "reduction_rate_percent": reduction_pct,
            "prevented_no_shows_monthly": int(prevented),
            "annual_savings": round(annual_savings, 2),
            "net_annual_benefit": round(net, 2),
            "roi_percent": round(roi, 2)
        })
    return {"scenarios": results}
