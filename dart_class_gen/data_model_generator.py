"""Data Model generator, could generate the dark class with specified method
that which storage class has"""

from loguru import logger
import pyperclip as clipboard

# models
from .models import GenerateInfo, GenerateResInfo, Member
from . import methods


def generate(gen_info: GenerateInfo):
    """Generate the Dart class string based on the gen_info"""
    if len(gen_info.member_list) < 1:
        e = Exception(
            f"To generate a dart class, you must provide "
            "at least one member, however the "
            "member list is empty in this GenerateInfo"
        )
        logger.error(e)
        raise e

    gen_res_info: GenerateResInfo = GenerateResInfo()

    # add comment if have
    if gen_info.comment is not None:
        gen_res_info.new_line(f"/// {gen_info.comment}")

    # first is the name part
    gen_res_info.add(f"class {gen_info.classname} " + "{")
    gen_res_info.itd()

    # add the field
    for member in gen_info.member_list:
        if member.comment is not None:
            gen_res_info.new_line(f"/// {member.comment}")
        nullable_mark: str = ""
        if member.nullable == True:
            nullable_mark += "?"
        # all list type member should be initialized as an empty list
        if member.is_list == True:
            gen_res_info.new_line(f"List<{member.type_name}> {member.identifier} = [];")
        else:
            gen_res_info.new_line(
                f"{member.type_name}{nullable_mark} {member.identifier};"
            )

    # default constructor
    gen_res_info.new_line()
    gen_res_info.new_line(f"{gen_info.classname}(" + "{")
    gen_res_info.itd()
    for member in gen_info.member_list:
        require_mark: str = ""
        if member.nullable == False:
            require_mark += "required "
        default_value_mark: str = ""
        if member.default_value is not None:
            # because required named fied can not have default value
            # clear the required mark before set default value
            require_mark = ""
            default_value_mark += " = "
            default_value_mark += member.default_value
        # the memeber is list type, so it must already set to [] before
        # here just skip this param
        if member.is_list == True:
            continue
        gen_res_info.new_line(
            f"{require_mark}this.{member.identifier}{default_value_mark}, "
        )
    gen_res_info.dtd()
    gen_res_info.new_line("});")

    # toMap
    methods.toMap(gen_info, gen_res_info)

    # from map
    methods.fromMap(gen_info, gen_res_info)

    # toJson
    methods.fromJson(gen_info, gen_res_info)

    # fromJson
    methods.toJson(gen_info, gen_res_info)

    # copyWith
    methods.copyWith(gen_info, gen_res_info)

    # end generator
    gen_res_info.dtd()
    gen_res_info.new_line("}")

    return gen_res_info.get_res()


if __name__ == "__main__":
    info = GenerateInfo()
    info.classname = "BangumiDetailedEpInfo"
    info.member_list = [
        Member(
            "name",
            "String",
            comment="Name of this ep",
            default_value='""',
        ),
        Member(
            "nameCn",
            "String",
            comment="Chinese name of this ep, can be null",
            nullable=True,
        ),
    ]

    info2: GenerateInfo = GenerateInfo()
    info2.classname = "BangumiAllEpsInfo"
    info2.member_list = [
        Member(
            "bgmId",
            "int",
            "0",
        ),
        Member(
            "epsList",
            "BangumiDetailedEpInfo",
            is_list=True,
            is_class=True,
        ),
    ]

    # do generate work here
    generated_class_str: str = generate(gen_info=info2)
    print(generated_class_str)
    clipboard.copy(generated_class_str)
