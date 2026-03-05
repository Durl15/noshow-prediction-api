from integrations import HubSpotClient, NoShowROIIntegration

# Test connection
client = HubSpotClient()
result = client.test_connection()
print('Connection result:', result)

# Calculate ROI
roi = NoShowROIIntegration()
result = roi.calculate_no_show_roi(200, 25, 100)
print('ROI result:', result)
