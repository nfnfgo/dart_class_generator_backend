"""Store the generator of different methods, e.g.:toMap()"""

# loggers
from loguru import logger

# models
from .models import GenerateInfo, GenerateResInfo


def toMap(gen_info: GenerateInfo, gen_res_info: GenerateResInfo) -> str:
    gen_res_info.new_line()
    gen_res_info.new_line("Map<String, dynamic> toMap(){")
    gen_res_info.itd()
    gen_res_info.new_line("Map<String, dynamic> infoMap = {};")
    for member in gen_info.member_list:
        # if member is list[class] type, should changed to map list first
        if (member.is_class == True) and (member.is_list == True):
            # create the map list
            gen_res_info.new_line(f"List<Map> {member.identifier}MapList = [];")
            # loop to convert elem to map and put into the map list
            gen_res_info.new_line(
                f"for ({member.type_name} curElem in {member.identifier}) " + "{"
            )
            gen_res_info.itd()
            gen_res_info.new_line(f"{member.identifier}MapList.add(curElem.toMap());")
            gen_res_info.dtd()
            gen_res_info.new_line("}")
            gen_res_info.new_line(
                f"infoMap['{member.identifier}MapList'] = {member.identifier}MapList;"
            )
            continue
        to_map_mark: str = ""
        if member.is_class == True:
            to_map_mark = ".toMap()"
        nullable_mark: str = ""
        if member.nullable == True and member.is_class == True:
            nullable_mark = "?"
        gen_res_info.new_line(
            f"""infoMap['{member.identifier}'] ="""
            f""" {member.to_map_method}{nullable_mark}{to_map_mark};"""
        )
    gen_res_info.new_line()
    gen_res_info.new_line("return infoMap;")
    gen_res_info.dtd()
    gen_res_info.new_line()
    gen_res_info.add("}")


def fromMap(gen_info: GenerateInfo, gen_res_info: GenerateResInfo) -> str:
    gen_res_info.new_line()
    gen_res_info.new_line(f"{gen_info.classname} fromMap(Map infoMap)" + "{")
    gen_res_info.itd()
    for member in gen_info.member_list:
        gen_res_info.new_line("try {")
        gen_res_info.itd()
        # if the member is list<class> type, do special work
        if (member.is_class == True) and (member.is_list == True):
            # first clear the list before
            gen_res_info.new_line(f"{member.identifier} = [];")
            # loop the map and convert to class, then add it to instance
            gen_res_info.new_line(
                f"for (var curMap in infoMap['{member.identifier}MapList']) " + "{"
            )
            gen_res_info.itd()
            gen_res_info.new_line(
                f"{member.identifier}.add({member.type_name}().fromMap(curMap));"
            )
            gen_res_info.dtd()
            gen_res_info.new_line("}")
        else:
            if member.is_class == True:
                nullable_mark: str = ""
                if member.nullable == True:
                    nullable_mark = "?"
                gen_res_info.new_line(
                    f"""{member.identifier}{nullable_mark}.fromMap(infoMap['{member.identifier}']);"""
                )
            else:
                gen_res_info.new_line(
                    f"""{member.identifier} = infoMap['{member.identifier}'];"""
                )
        gen_res_info.dtd()
        gen_res_info.new_line("} catch (e) {")
        gen_res_info.itd()
        gen_res_info.new_line(
            f"""debugPrint('[FailedToReadFromMap] Failed to update member {member.identifier}');"""
        )
        gen_res_info.dtd()
        gen_res_info.new_line("}")
    gen_res_info.new_line()
    gen_res_info.new_line("return this;")
    gen_res_info.dtd()
    gen_res_info.new_line("}")


def toJson(gen_info: GenerateInfo, gen_res_info: GenerateResInfo) -> str:
    gen_res_info.new_line()
    gen_res_info.new_line("/// Returns a serialized json string of this instance")
    gen_res_info.new_line("String toJson() {")
    gen_res_info.itd()
    gen_res_info.new_line("return jsonEncode(toMap());")
    gen_res_info.dtd()
    gen_res_info.new_line("}")


def fromJson(gen_info: GenerateInfo, gen_res_info: GenerateResInfo) -> str:
    gen_res_info.new_line()
    gen_res_info.new_line(
        "/// Update the info of this instance based on the json string input"
    )
    gen_res_info.new_line(f"{gen_info.classname} fromJson(String? jsonStr) " + "{")
    gen_res_info.itd()
    gen_res_info.new_line("if(jsonStr == null) {")
    gen_res_info.itd()
    gen_res_info.new_line("return this;")
    gen_res_info.dtd()
    gen_res_info.new_line("}")
    gen_res_info.new_line("Map infoMap = jsonDecode(jsonStr);")
    gen_res_info.new_line("fromMap(infoMap);")
    gen_res_info.new_line("return this;")
    gen_res_info.dtd()
    gen_res_info.new_line("}")


def copyWith(gen_info: GenerateInfo, gen_res_info: GenerateResInfo) -> str:
    gen_res_info.new_line(
        f"{gen_info.classname} copyWith({gen_info.classname} other)" + " {"
    )
    gen_res_info.itd()
    for member in gen_info.member_list:
        # if member is another class type, use copyWith method
        if member.is_class == True and member.is_list == False:
            # if this field is nullable, than do extra deal with it
            if member.nullable == True:
                # make sure other.identifier is available before use
                gen_res_info.new_line(f"if (other.{member.identifier} == null)" + " {")
                gen_res_info.itd()
                gen_res_info.new_line(f"{member.identifier} = null;")
                gen_res_info.dtd()
                gen_res_info.new_line("} else {")
                gen_res_info.itd()
                # if other is not null, but this is null, then first
                # create default ins for this ins
                gen_res_info.new_line(f"if ({member.identifier} == null)" + " {")
                gen_res_info.itd()
                gen_res_info.new_line(f"{member.identifier} = {member.type_name}();")
                gen_res_info.dtd()
                gen_res_info.new_line("}")
                gen_res_info.new_line(
                    f"{member.identifier}!.copyWith(other!.{member.identifier});"
                )
                gen_res_info.dtd()
                gen_res_info.new_line("}")

        # if it is list and class type
        elif (member.is_list == True) and (member.is_class == True):
            # first, clean the list in this class
            gen_res_info.new_line(f"{member.identifier} = [];")
            # then

        else:
            gen_res_info.new_line(
                f"{member.identifier} = other.{member.identifier} ?? this.{member.identifier};"
            )

        gen_res_info.dtd()
        gen_res_info.new_line("}")
