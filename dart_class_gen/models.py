"""Classes used by this program"""

# fundamental
from pydantic import BaseModel

# logger
from loguru import logger


class Member:
    # the identifier of this member, will used as a keyword in dart class
    identifier: str = ""
    # the type name of this member, usually will be a dart supported type
    type_name: str = ""
    # default value of the member, if null, this member will be consider nullable
    default_value: str | None = None
    # toMap method of this member, default to `toString()`
    to_map_method: str = ""
    # comment of this member field, could be None
    comment: str | None = None
    # if this field is nullable
    # we strongly recommend not to set nullable for a class member
    nullable: bool | None = None
    # if this member is a class, if True, it will consider this member has toMap/fromMap method
    is_class: bool | None = None
    # if this memeber is a list
    is_list: bool | None = None

    def __init__(
        self,
        identifier: str,
        type_name: str,
        default_value: str | None = None,
        comment: str | None = None,
        nullable: bool | None = None,
        is_class: bool = False,
        is_list: bool = False,
    ) -> None:
        self.identifier = identifier
        self.type_name = type_name
        self.to_map_method = self.identifier
        self.default_value = default_value
        self.comment = comment
        self.is_class = is_class
        self.is_list = is_list
        # if nullable has not assigned when initializing
        # set the nullable status based on if this member
        # has default value
        if nullable is None:
            nullable = False
            if default_value is None and is_list == False:
                logger.warning(
                    "[NullableButNoDefault] "
                    f"Can NOT set a member {identifier} to nullable when this member "
                    "has no default value.\n"
                    "If you want this member to be nullable, try to give it a default "
                    "value by setting Member.default_value field"
                )
                nullable = True
        self.nullable = nullable

    def get_null_mark(self):
        """
        Return '?' if this member is actually can be null ,else return
        empty string

        Notice:
        - This method will return empty string even the `nullable` is `True` when
        this member `is_list` is `True`, since the list member will always has
        default value of `[]` (an empty list) in this program
        """
        if (self.nullable == True) and (self.is_list == False):
            return "?"
        return ""


class GenerateInfo:
    """
    The class that contains all info needed to generate
    a new dart class
    """

    # name of this class
    classname: str = "NewDartClass"
    # the comment of this class, will be add to generated class string
    comment: str | None = None
    # members of this class
    member_list: list[Member] = None

    def __init__(
        self,
        member_list: list[Member] | None = None,
        comment: str | None = None,
    ) -> None:
        self.member_list = []
        if member_list is not None:
            self.member_list = member_list
        if comment is not None:
            self.comment = comment


class GenerateResInfo:
    """Store the generated class info, also provide methods to
    operate the generated class string and the intend level"""

    # store the generated class string
    gen_class_str: str = ""
    # store the current intend layer level
    intend_level: int = 0

    def add(self, new_str: str | None = None) -> "GenerateResInfo":
        """Directly add strings to the current line of the
        generated class string

        Params:
        - new_str: The string you want to add

        Notice:
        - Will do nothing and return directly if the new_str is None
        without raise error"""
        if new_str is None:
            return self
        self.gen_class_str += new_str
        return self

    def __add_intend(self) -> "GenerateResInfo":
        """Add intend to the current generated string based on the
        current intend level

        Notice:
        - Generally this method should not be called directly, and is
        only used by methods like new_line()"""
        self.gen_class_str += "".join(["  " for i in range(self.intend_level)])
        return self

    def new_line(
        self,
        new_str: str | None = None,
        intend: bool = True,
    ) -> "GenerateResInfo":
        """Create a new line and add string to this line

        Params:
        - `new_str` The string that you want to add to the new line
        - `intend` Default true, will add intend when creating the
        new line
        """
        # first changeline
        self.gen_class_str += "\n"
        # add intend if needed
        if intend == True:
            self.__add_intend()
        # add string
        self.add(new_str=new_str)
        return self

    def itd(self) -> "GenerateResInfo":
        """Add the intend level by one"""
        self.intend_level += 1
        return self

    def dtd(self) -> "GenerateResInfo":
        """Decrease the intend level by one"""
        self.intend_level -= 1
        return self

    def get_res(self) -> str:
        """Get the current generated string"""
        return self.gen_class_str
