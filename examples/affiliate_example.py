from blofin.client import Client
from blofin.rest_affiliate import AffiliateAPI
from datetime import datetime, timedelta

def affiliate_example():
    """Example of using RestAffiliateAPI for affiliate operations."""
    
    # Replace these with your API credentials
    api_key = "...."
    secret_key = "...."
    passphrase = "...."
    
    client = Client(api_key, secret_key, passphrase)
    affiliate_api = AffiliateAPI(client)
    
    try:
        # 1. Get basic affiliate information
        basic_info = affiliate_api.getBasicInfo()
        print("\n=== Basic Affiliate Information ===")
        print(basic_info)
        
        # Calculate timestamps for last 30 days
        end_time = int(datetime.now().timestamp() * 1000)  # Current time in milliseconds
        begin_time = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)  # 30 days ago
        
        # 2. Get direct invitees list (last 30 days, up to 10 records)
        invitees = affiliate_api.getInvitees(
            begin=str(begin_time),
            end=str(end_time),
            limit="10"
        )
        print("\n=== Direct Invitees (Last 30 Days) ===")
        print(invitees)
        
        # 3. Get sub-invitees list (last 30 days, up to 10 records)
        sub_invitees = affiliate_api.getSubInvitees(
            begin=str(begin_time),
            end=str(end_time),
            limit="10"
        )
        print("\n=== Sub-Invitees (Last 30 Days) ===")
        print(sub_invitees)
        
        # 4. Get sub-affiliates list (last 30 days, up to 10 records)
        sub_affiliates = affiliate_api.getSubAffiliates(
            begin=str(begin_time),
            end=str(end_time),
            limit="10"
        )
        print("\n=== Sub-Affiliates (Last 30 Days) ===")
        print(sub_affiliates)
        
        # 5. Get daily commission data (last 30 days)
        daily_commission = affiliate_api.getInviteesDailyCommission(
            begin=str(begin_time),
            end=str(end_time),
            limit="30"  # Get data for each day
        )
        print("\n=== Daily Commission Data (Last 30 Days) ===")
        print(daily_commission)
        
        # Example of filtering by specific UID
        specific_uid = "12345"  # Replace with actual UID
        
        # 6. Get invitee information for specific UID
        specific_invitee = affiliate_api.getInvitees(uid=specific_uid)
        print(f"\n=== Invitee Information for UID {specific_uid} ===")
        print(specific_invitee)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    affiliate_example()
