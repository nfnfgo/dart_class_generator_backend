from pydantic import BaseModel


class ResponseInfoBase(BaseModel):
    """
    Base model of response info
    """

    # If the response is valid and success, default `True`
    success: bool = True

    # Error message of this respones, if success is False,
    # then this param may contains error info
    err_msg: str | None = None

    def set_err(self, err_msg: str | None):
        """Set this response to error status with specified err msg"""
        self.err_msg = err_msg
        self.success = False

    def set_succ(self):
        """Set this respone to success and clear err msg"""
        self.success = True
        self.err_msg = None


class DartClassGenResInfo(ResponseInfoBase):
    """Model response class for dart class generate result"""

    generate_class_str: str | None = None

    def set_res(self, gen_str: str = None) -> "DartClassGenResInfo":
        """
        Initialize a dart class generate result

        Params:
        - `gen_str` Create a response with gen_str if it's not
        null, else, create a failed response
        """

        # if the string is None, means generate failed
        if gen_str is None:
            self.set_err("[GenerateFailed]")
        # if success to gen string, update the response
        else:
            self.set_succ()
            self.generate_class_str = gen_str
        return self
