from integrations.app.hubspot_client import HubSpotClient
import requests
import os

class NoShowROIIntegration:
    def __init__(self):
        self.hs_client = HubSpotClient()
    
    def calculate_no_show_roi(self, appointment_value, no_show_rate, monthly_appointments):
        """Calculate potential ROI from reducing no-shows"""
        current_no_shows = monthly_appointments * (no_show_rate / 100)
        current_lost_revenue = current_no_shows * appointment_value
        
        # Assume 30% reduction in no-shows with prediction tool
        improved_no_shows = current_no_shows * 0.7
        recovered_revenue = (current_no_shows - improved_no_shows) * appointment_value
        
        return {
            'monthly_appointments': monthly_appointments,
            'current_no_show_rate': no_show_rate,
            'current_lost_revenue': current_lost_revenue,
            'projected_improvement': '30%',
            'recovered_revenue': recovered_revenue,
            'annual_impact': recovered_revenue * 12
        }
    
    def sync_roi_to_hubspot(self, company_id, roi_data):
        """Sync ROI calculation to HubSpot company record"""
        properties = {
            'no_show_current_rate': str(roi_data['current_no_show_rate']),
            'no_show_monthly_lost_revenue': str(roi_data['current_lost_revenue']),
            'no_show_projected_recovery': str(roi_data['recovered_revenue']),
            'no_show_annual_impact': str(roi_data['annual_impact'])
        }
        
        try:
            response = requests.patch(
                f'{self.hs_client.base_url}/crm/v3/objects/companies/{company_id}',
                headers=self.hs_client._get_headers(),
                json={'properties': properties}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Failed to sync to HubSpot: {e}')
            return None

if __name__ == '__main__':
    integration = NoShowROIIntegration()
    roi = integration.calculate_no_show_roi(
        appointment_value=150,
        no_show_rate=20,
        monthly_appointments=100
    )
    print('No-Show ROI Analysis:')
    print(f'Current monthly lost revenue: ')
    print(f'Projected monthly recovery: ')
    print(f'Annual impact: ')
