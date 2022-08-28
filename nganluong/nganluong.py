import hashlib
import urllib.parse

class NganLuong:
    responseData = {}
    def __init__(self,merchant_site_code,secure_pass,return_url,receiver,cancel_url,api_url):
        self.merchant_site_code = merchant_site_code
        self.secure_pass= secure_pass
        self.receiver = receiver
        self.return_url= return_url
        self.cancel_url = cancel_url
        self.api_url = api_url
    def get_payment_url(self, requestData):
        inputData = sorted(requestData.items())
        queryString = f'merchant_site_code={self.merchant_site_code}&return_url={self.return_url}&receiver={self.receiver}'
        for key, val in inputData:
            queryString = queryString + "&" + key + '=' + urllib.parse.quote_plus(str(val))
        data = self.merchant_site_code + ' ' + self.return_url + ' ' + self.receiver+ ' '\
        + str(requestData['transaction_info'])\
        + ' ' + str(requestData['order_code'])\
        + ' ' + str(requestData['price'])\
        + ' ' + str(requestData['currency']) \
        + ' ' + str(requestData['quantity'])\
        + ' ' + str(requestData['tax'])\
        + ' ' + str(requestData['discount']) \
        + ' ' + str(requestData['fee_cal'])\
        + ' ' + str(requestData['fee_shipping']) \
        + ' ' + str(requestData['order_description']) \
        + ' ' + str(requestData['buyer_info']) \
        + ' ' + str(requestData['affiliate_code'])\
        + ' ' + self.secure_pass
        hashValue = self.__hashmd5(data)
        return self.api_url  + "?" + queryString + '&secure_code=' + hashValue

    def validate_response(self,responseData):
       
        verify_secure_code = ' ' + responseData['transaction_info'] + ' ' + responseData['order_code'] + ' ' + responseData['price'] + ' ' + responseData['payment_id'] + ' ' +\
            responseData['payment_type'] + ' ' + responseData['error_text'] + ' ' + self.merchant_site_code + ' ' + self.secure_pass
        verify_secure_code = self.__hashmd5(verify_secure_code)
        return verify_secure_code == responseData['secure_code']

    @staticmethod
    def __hashmd5(data):
        return hashlib.md5(data.encode()).hexdigest()
