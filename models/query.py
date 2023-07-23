"""
Classes used as the received query model

We do NOT directly use the model inside the dart_class_gen, since the model 
inside dart_class_gen has it's own __init__ method, which will cause problems 
when those class are set to inherited from pydantic.BaseModel

Also, the API Backend should not affect the class sturcture of the dart_gen_class, 
so it's better choice to create a new QueryInfo model class in this file which is 
inherited from pydantic.BaseModel, and provide the method to convert this QueryModel 
to the dargen classes
"""

# fundamentals
from pydantic import BaseModel

# dartgen
import dart_class_gen as dartgen


class MemberQueryInfo(BaseModel):
    """
    The member class used as the query model
    """

    # the identifier of this member, will used as a keyword in dart class
    identifier: str
    # the type name of this member, usually will be a dart supported type
    type_name: str
    # default value of the member, if null, this member will be consider nullable
    default_value: str | None = None
    # comment of this member field, could be None
    comment: str | None = None
    # if this field is nullable
    # we strongly recommend not to set nullable for a class member
    nullable: bool | None = False
    # if this member is a class, if True, it will consider this member has toMap/fromMap method
    is_class: bool | None = False
    # if this memeber is a list
    is_list: bool | None = False

    def to_member_class(self) -> dartgen.models.Member:
        """Returns a Member class from this pydantic instance"""
        return dartgen.models.Member(
            identifier=self.identifier,
            type_name=self.type_name,
            default_value=self.default_value,
            comment=self.comment,
            nullable=self.nullable,
            is_class=self.is_class,
            is_list=self.is_list,
        )


class DartGenQueryInfo(BaseModel):
    # name of this class
    classname: str = "NewDartClass"
    # the comment of this class, will be add to generated class string
    comment: str | None = None
    # members of this class
    member_list: list[MemberQueryInfo]

    def to_gen_class(self) -> dartgen.models.GenerateInfo:
        dart_gen_class = dartgen.models.GenerateInfo()
        dart_gen_class.classname = self.classname
        dart_gen_class.comment = self.comment
        # init list, and convert this query list to the member list
        dart_gen_class.member_list = []
        for member_query in self.member_list:
            dart_gen_class.member_list.append(member_query.to_member_class())
        return dart_gen_class
