from typing import Dict, Optional
from .client import Client

class AffiliateAPI:
    """BloFin Affiliate REST API client.
    
    Handles all affiliate-related endpoints including referral codes, invitees management,
    and affiliate statistics.
    """
    
    def __init__(self, client: Client):
        self._client = client

    def getReferralCode(self) -> Dict:
        """Get affiliate's referral code list.
        
        Returns:
            Dict: Response containing referral code information with fields:
                - code: Response code
                - msg: Response message
                - data: List of referral codes, each containing:
                    - referralCode: The referral code
                    - commissionRate: Total commission rate
                    - cashbackRate: Cashback rate for invitees
                    - invitees: Total invitees invited with this code
                    - remark: Additional remarks
                    - isDefaultReferralCode: Whether this is the default code (true/false)
                    - makerFeeRate: Futures maker fee rate for invitees
                    - takerFeeRate: Futures taker fee rate for invitees
                    - referralLink: The referral link URL
        """
        return self._client.get('/api/v1/affiliate/referral-code')

    def getInvitees(
        self,
        uid: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get list of direct invitees for the affiliate account.
        
        Args:
            uid: Optional, filter by invitee's UID
            after: Optional, return records earlier than this ID for pagination
            before: Optional, return records newer than this ID for pagination
            begin: Optional, filter begin timestamp in milliseconds (Unix timestamp format, e.g. 1597026383085)
            end: Optional, filter end timestamp in milliseconds (Unix timestamp format, e.g. 1597026383085)
            limit: Optional, number of results per request (max 30, default 10)
            
        Returns:
            Dict: Response containing invitee information with fields:
                - code: Response code
                - msg: Response message
                - data: List of invitees, each containing:
                    - id: ID of the record
                    - uid: UID of invitee
                    - registerTime: Register time in milliseconds (Unix timestamp)
                    - totalTradingVolume: Total futures trading amount
                    - totalTradingFee: Total futures trading fee
                    - totalCommision: Total commission
                    - totalDeposit: Total deposit amount
                    - totalWithdrawal: Total withdrawal amount
                    - kycLevel: KYC level (0: Non KYC, 1: Personal info verified, 2: Address proof verified)
                    - equity: Total equity across all accounts in USDT
        """
        params = {}
        if uid:
            params["uid"] = uid
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if begin:
            params["begin"] = begin
        if end:
            params["end"] = end
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/affiliate/invitees', None if not params else params)

    def getSubInvitees(
        self,
        uid: Optional[str] = None,
        subAffiliateUid: Optional[str] = None,
        subAffiliateLevel: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get information about sub-affiliate invitees.
        
        Args:
            uid: Optional, Invitee's UID
            subAffiliateUid: Optional, Sub affiliate's UID
            subAffiliateLevel: Optional, Sub affiliate's level (2/3/4)
            after: Optional, Return records earlier than this ID
            before: Optional, Return records newer than this ID
            begin: Optional, Filter begin timestamp in milliseconds
            end: Optional, Filter end timestamp in milliseconds
            limit: Optional, Number of results per request (max 30, default 10)
            
        Returns:
            Dict: Response containing sub-invitee information:
                - code: Response code
                - msg: Response message
                - data: List of invitees, each containing:
                    - id: ID
                    - uid: UID of invitee
                    - subAffiliateUid: UID of sub affiliate
                    - subAffiliateLevel: Level of invitee
                    - registerTime: Register time in milliseconds
                    - totalTradingVolume: Total futures trading amount
                    - totalTradingFee: Total futures trading fee
                    - totalCommision: Total commission
                    - totalDeposit: Total deposit amount
                    - totalWithdrawal: Total withdrawal amount
                    - kycLevel: KYC level (0/1/2)
                    - equity: Total equity across all accounts in USDT
                    
        Note:
            For timestamps:
            - Use Unix timestamp format in milliseconds, e.g. 1597026383085
            
            For KYC levels:
            - 0: Non KYC
            - 1: Complete personal information verification
            - 2: Complete address proof verification
            
        Examples:
            >>> # Get all sub-invitees
            >>> api.getSubInvitees()
            
            >>> # Get invitees for specific sub-affiliate
            >>> api.getSubInvitees(subAffiliateUid="30285102093")
            
            >>> # Get invitees with time filter and pagination
            >>> api.getSubInvitees(
            ...     subAffiliateLevel="2",
            ...     begin="1706861990475",
            ...     limit="20"
            ... )
        """
        params = {}
        if uid:
            params["uid"] = uid
        if subAffiliateUid:
            params["subAffiliateUid"] = subAffiliateUid
        if subAffiliateLevel:
            params["subAffiliateLevel"] = subAffiliateLevel
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if begin:
            params["begin"] = begin
        if end:
            params["end"] = end
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/affiliate/sub-invitees', params=params)

    def getSubAffiliates(
        self,
        subAffiliateUid: Optional[str] = None,
        subAffiliateLevel: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get information about sub-affiliates.
        
        Args:
            subAffiliateUid: Optional, Sub affiliate's UID
            subAffiliateLevel: Optional, Sub affiliate's level (2/3/4)
            after: Optional, Return records earlier than this ID
            before: Optional, Return records newer than this ID
            begin: Optional, Filter begin timestamp in milliseconds
            end: Optional, Filter end timestamp in milliseconds
            limit: Optional, Number of results per request (max 100, default 10)
            
        Returns:
            Dict: Response containing sub-affiliate information:
                - code: Response code
                - msg: Response message
                - data: List of sub-affiliates, each containing:
                    - id: ID
                    - uid: UID of sub affiliate
                    - commissionRate: Commission rate
                    - createTime: Creation time in milliseconds
                    - upperAffiliate: Upper affiliate's UID
                    - invitees: Total number of invitees
                    - totalTradedUsers: Total traded invitees
                    - totalTradingVolume: Total futures trading volume
                    - totalTradingFee: Total futures trading fee
                    - totalCommision: Total commission
                    - myCommision: Commission received from sub affiliate
                    - tag: Tag
                    - kycLevel: KYC level (0/1/2)
                    
        Note:
            For timestamps:
            - Use Unix timestamp format in milliseconds, e.g. 1597026383085
            
            For KYC levels:
            - 0: Non KYC
            - 1: Complete personal information verification
            - 2: Complete address proof verification
            
        Examples:
            >>> # Get all sub-affiliates
            >>> api.getSubAffiliates()
            
            >>> # Get sub-affiliates by level
            >>> api.getSubAffiliates(subAffiliateLevel="2")
            
            >>> # Get sub-affiliates with pagination and time filter
            >>> api.getSubAffiliates(
            ...     limit="20",
            ...     begin="1707018797957",
            ...     end="1707018897957"
            ... )
        """
        params = {}
        if subAffiliateUid:
            params["subAffiliateUid"] = subAffiliateUid
        if subAffiliateLevel:
            params["subAffiliateLevel"] = subAffiliateLevel
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if begin:
            params["begin"] = begin
        if end:
            params["end"] = end
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/affiliate/sub-affiliates', None if not params else params)

    def getBasicInfo(self) -> Dict:
        """Get affiliate's basic information.
        
        Returns:
            Dict: Response containing basic information with fields:
                - commissionRate: Total commission rate
                - cashbackRate: Cashback rate
                - totalCommission: Cumulative commission of all-level sub-invitees (updated every 6 hours)
                - referralCode: Default referral code
                - referralLink: Default referral link
                - directInvitees: Total invitees invited by user
                - subInvitees: Total invitees invited by sub-affiliates
                - tradeInvitees: Number of traded users of invitees (both direct and sub)
                - updateTime: Update time of data in milliseconds
                - totalTradingVolume: Cumulative total trading volume of all invitees
                - directCommission7d: Total Commission from direct invitees in last 7 days
                - directCommission30d: Total Commission from direct invitees in last 30 days
                - subCommission7d: Total Commission from sub-invitees in last 7 days
                - subCommission30d: Total Commission from sub-invitees in last 30 days
                - directInvitee7d: Number of direct invitees in last 7 days
                - directInvitee30d: Number of direct invitees in last 30 days
                - subInvitee7d: Number of sub-invitees in last 7 days
                - subInvitee30d: Number of sub-invitees in last 30 days
        """
        return self._client.get('/api/v1/affiliate/basic')

    def getInviteesDailyCommission(
        self,
        uid: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        begin: Optional[str] = None,
        end: Optional[str] = None,
        limit: Optional[str] = None
    ) -> Dict:
        """Get daily commission data of direct invitees.
        
        Args:
            uid: Optional, Invitee's UID (Required if only using begin/end pagination)
            after: Optional, Return records earlier than this ID
            before: Optional, Return records newer than this ID
            begin: Optional, Filter begin timestamp in milliseconds (Unix timestamp)
            end: Optional, Filter end timestamp in milliseconds (Unix timestamp)
            limit: Optional, Number of results per request (max 100, default 10)
            
        Returns:
            Dict: Response containing daily commission data:
                - code: Response code
                - msg: Response message
                - data: List of commission records, each containing:
                    - id: Record ID
                    - uid: Invitee's UID
                    - commission: Daily commission amount
                    - commissionTime: Commission time in milliseconds
                    - cashback: Cashback amount
                    - fee: Daily trading fee
                    - kycLevel: KYC level (0: Non KYC, 1: Personal info verified, 2: Address verified)
                    
        Note:
            When using only begin/end parameters for pagination, uid parameter is required
            to ensure data accuracy.
        """
        params = {}
        if uid:
            params["uid"] = uid
        if after:
            params["after"] = after
        if before:
            params["before"] = before
        if begin:
            params["begin"] = begin
        if end:
            params["end"] = end
        if limit:
            params["limit"] = limit
            
        return self._client.get('/api/v1/affiliate/invitees/daily', None if not params else params)
