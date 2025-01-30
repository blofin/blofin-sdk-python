"""
Affiliate API Example
"""
from blofin.client import Client
from blofin.rest_affiliate import AffiliateAPI
from datetime import datetime, timedelta

def affiliateExample():
    """Example of using RestAffiliateAPI for affiliate operations."""
    
    # Replace these with your API credentials
    apiKey = "...."
    secretKey = "...."
    passphrase = "...."
    
    client = Client(apiKey=apiKey, apiSecret=secretKey, passphrase=passphrase)
    affiliateApi = AffiliateAPI(client)
    
    try:
        # 1. Get basic affiliate information
        basicInfo = affiliateApi.getBasicInfo()
        print("\n=== Basic Affiliate Information ===")
        print(basicInfo)
        
        # Calculate timestamps for last 30 days
        endTime = int(datetime.now().timestamp() * 1000)  # Current time in milliseconds
        beginTime = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)  # 30 days ago
        
        # 2. Get direct invitees list (last 30 days, up to 10 records)
        invitees = affiliateApi.getInvitees(
            begin=str(beginTime),
            end=str(endTime),
            limit="10"
        )
        print("\n=== Direct Invitees (Last 30 Days) ===")
        print(invitees)
        
        # 3. Get sub-invitees list (last 30 days, up to 10 records)
        subInvitees = affiliateApi.getSubInvitees(
            begin=str(beginTime),
            end=str(endTime),
            limit="10"
        )
        print("\n=== Sub-Invitees (Last 30 Days) ===")
        print(subInvitees)
        
        # 4. Get sub-affiliates list (last 30 days, up to 10 records)
        subAffiliates = affiliateApi.getSubAffiliates(
            begin=str(beginTime),
            end=str(endTime),
            limit="10"
        )
        print("\n=== Sub-Affiliates (Last 30 Days) ===")
        print(subAffiliates)
        
        # 5. Get daily commission data (last 30 days)
        dailyCommission = affiliateApi.getInviteesDailyCommission(
            begin=str(beginTime),
            end=str(endTime),
            limit="30"  # Get data for each day
        )
        print("\n=== Daily Commission Data (Last 30 Days) ===")
        print(dailyCommission)
        
        # Example of filtering by specific UID
        specificUid = "12345"  # Replace with actual UID
        
        # 6. Get invitee information for specific UID
        specificInvitee = affiliateApi.getInvitees(uid=specificUid)
        print(f"\n=== Invitee Information for UID {specificUid} ===")
        print(specificInvitee)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    affiliateExample()
