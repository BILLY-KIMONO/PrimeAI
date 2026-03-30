import os
import requests
import base64
import json
from datetime import datetime
from typing import Optional, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# ============= M-Pesa Integration =============

class MPesaService:
    """M-Pesa payment service for Kenyan payments"""
    
    BASE_URL = "https://sandbox.safaricom.co.ke"  # Use live URL in production
    
    def __init__(self):
        self.consumer_key = os.getenv("MPESA_CONSUMER_KEY", "")
        self.consumer_secret = os.getenv("MPESA_CONSUMER_SECRET", "")
        self.shortcode = os.getenv("MPESA_SHORTCODE", "174379")  # Test shortcode
        self.passkey = os.getenv("MPESA_PASSKEY", "bfb279f9aa9bdbcf158e97dd1a2c6f95")  # Test passkey
        self.callback_url = os.getenv("MPESA_CALLBACK_URL", "https://api.primeai.com/api/payments/mpesa/callback")
    
    def get_access_token(self) -> Optional[str]:
        """Get M-Pesa access token"""
        try:
            auth_url = f"{self.BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
            credentials = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
            
            headers = {
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(auth_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.json().get("access_token")
        except Exception as e:
            logger.error(f"Failed to get M-Pesa token: {str(e)}")
            return None
    
    def stk_push(self, phone_number: str, amount: float, account_ref: str, description: str) -> Dict[str, Any]:
        """Initiate M-Pesa STK push payment"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {"success": False, "error": "Failed to authenticate with M-Pesa"}
            
            # Format phone number (ensure it starts with 254)
            phone = phone_number.replace("+", "").replace(" ", "")
            if not phone.startswith("254"):
                phone = "254" + phone.lstrip("0")
            
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode(
                f"{self.shortcode}{self.passkey}{timestamp}".encode()
            ).decode()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": int(amount),
                "PartyA": phone,
                "PartyB": self.shortcode,
                "PhoneNumber": phone,
                "CallBackURL": self.callback_url,
                "AccountReference": account_ref,
                "TransactionDesc": description
            }
            
            response = requests.post(
                f"{self.BASE_URL}/mpesa/stkpush/v1/processrequest",
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": result.get("ResponseCode") == "0",
                "checkout_request_id": result.get("CheckoutRequestID"),
                "response_code": result.get("ResponseCode"),
                "response_message": result.get("ResponseDescription")
            }
        except Exception as e:
            logger.error(f"M-Pesa STK push failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def query_transaction(self, checkout_request_id: str) -> Dict[str, Any]:
        """Query M-Pesa transaction status"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {"success": False, "error": "Failed to authenticate with M-Pesa"}
            
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            password = base64.b64encode(
                f"{self.shortcode}{self.passkey}{timestamp}".encode()
            ).decode()
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }
            
            response = requests.post(
                f"{self.BASE_URL}/mpesa/stkpushquery/v1/query",
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": result.get("ResponseCode") == "0",
                "result_code": result.get("ResultCode"),
                "result_desc": result.get("ResultDesc"),
                "merchant_request_id": result.get("MerchantRequestID")
            }
        except Exception as e:
            logger.error(f"M-Pesa query failed: {str(e)}")
            return {"success": False, "error": str(e)}


# ============= PayPal Integration =============

class PayPalService:
    """PayPal payment service"""
    
    BASE_URL = "https://api.sandbox.paypal.com"  # Use live URL in production
    
    def __init__(self):
        self.client_id = os.getenv("PAYPAL_CLIENT_ID", "")
        self.client_secret = os.getenv("PAYPAL_CLIENT_SECRET", "")
        self.merchant_email = os.getenv("PAYPAL_MERCHANT_EMAIL", "billykimono@gmail.com")
    
    def get_access_token(self) -> Optional[str]:
        """Get PayPal access token"""
        try:
            auth = (self.client_id, self.client_secret)
            data = {"grant_type": "client_credentials"}
            
            response = requests.post(
                f"{self.BASE_URL}/v1/oauth2/token",
                auth=auth,
                data=data,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json().get("access_token")
        except Exception as e:
            logger.error(f"Failed to get PayPal token: {str(e)}")
            return None
    
    def create_payment(self, amount: float, description: str, return_url: str, cancel_url: str) -> Dict[str, Any]:
        """Create PayPal payment"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {"success": False, "error": "Failed to authenticate with PayPal"}
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "transactions": [
                    {
                        "amount": {
                            "total": str(round(amount, 2)),
                            "currency": "USD",
                            "details": {
                                "subtotal": str(round(amount, 2))
                            }
                        },
                        "description": description,
                        "invoice_number": f"PRIME{datetime.now().timestamp()}"
                    }
                ],
                "redirect_urls": {
                    "return_url": return_url,
                    "cancel_url": cancel_url
                }
            }
            
            response = requests.post(
                f"{self.BASE_URL}/v1/payments/payment",
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract approval link
            approval_url = None
            for link in result.get("links", []):
                if link.get("rel") == "approval_url":
                    approval_url = link.get("href")
                    break
            
            return {
                "success": True,
                "payment_id": result.get("id"),
                "state": result.get("state"),
                "approval_url": approval_url
            }
        except Exception as e:
            logger.error(f"PayPal payment creation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def execute_payment(self, payment_id: str, payer_id: str) -> Dict[str, Any]:
        """Execute approved PayPal payment"""
        try:
            access_token = self.get_access_token()
            if not access_token:
                return {"success": False, "error": "Failed to authenticate with PayPal"}
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "payer_id": payer_id
            }
            
            response = requests.post(
                f"{self.BASE_URL}/v1/payments/payment/{payment_id}/execute",
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "success": result.get("state") == "approved",
                "transaction_id": result.get("id"),
                "state": result.get("state"),
                "payer_email": result.get("payer", {}).get("payer_info", {}).get("email")
            }
        except Exception as e:
            logger.error(f"PayPal payment execution failed: {str(e)}")
            return {"success": False, "error": str(e)}


# ============= Payment Service Factory =============

class PaymentService:
    """Main payment service coordinator"""
    
    def __init__(self):
        self.mpesa = MPesaService()
        self.paypal = PayPalService()
    
    def create_payment_url(self, method: str, amount: float, description: str, 
                           return_url: str, cancel_url: str) -> Dict[str, Any]:
        """Create payment URL based on method"""
        if method == "paypal":
            return self.paypal.create_payment(amount, description, return_url, cancel_url)
        elif method == "mpesa":
            return {"success": False, "error": "M-Pesa requires phone number"}
        else:
            return {"success": False, "error": f"Unsupported payment method: {method}"}
    
    def process_mpesa_payment(self, phone_number: str, amount: float, 
                             plan_type: str, user_id: int) -> Dict[str, Any]:
        """Process M-Pesa payment"""
        account_ref = f"USER{user_id}-{plan_type.upper()}"
        description = f"PrimeAI {plan_type.upper()} subscription"
        return self.mpesa.stk_push(phone_number, amount, account_ref, description)
