from antlr4 import FileStream, ParseTreeWalker
from gen.java.JavaLexer import JavaLexer
from listener import *


def get_file_names_in_dir(directory_name: str, filter=lambda x: x.endswith(".java")) -> list:
    result = []
    for (dir_name, dir_names, file_names) in os.walk(directory_name):
        result.extend([f'{dir_name}/{file_name}' for file_name in file_names if filter(file_name)])

    return result


def get_program(source_files: list, print_status=False) -> Program:
    program = Program()
    for file in source_files:
        if print_status:
            print(f'Parsing {file}')

        stream = FileStream(file, encoding='utf8')
        lexer = JavaLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = JavaParser(token_stream)
        tree = parser.compilationUnit()
        listener = UtilsListener(file)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        if listener.package.name not in program.packages:
            program.packages[listener.package.name] = listener.package
        else:
            for klass in listener.package.classes:
                program.packages[listener.package.name].classes[klass] = listener.package.classes[klass]

    return program


def get_classes_count(program: Program) -> int:
    result = 0
    for package in program.packages.values():
        result += len(package.classes)

    return result


def get_class_attrs(program: Program) -> dict:
    class_attrs = {}
    for package in program.packages.values():
        for klass in package.classes.values():
            class_attrs[klass.name] = {'methods': [], 'fields': []}

            for method in klass.methods.values():
                class_attrs[klass.name]['methods'].append(
                    {
                        'name': method.name,
                        'modifier': method.modifiers,
                    }
                )

            for field in klass.fields.values():
                class_attrs[klass.name]['fields'].append(
                    {
                        'name': field.name,
                        'modifier': field.modifiers,
                    }
                )

    return class_attrs


def get_class_invocations(program: Program) -> dict:
    class_instantiations = {}
    for package in program.packages.values():
        for klass in package.classes.values():
            if klass.name in class_instantiations.keys():
                class_instantiations[klass.name].extend(klass.class_invocations)
            else:
                class_instantiations[klass.name] = klass.class_invocations

    return class_instantiations


def get_method_invocations(program: Program) -> dict:
    method_invocations = {}
    for package in program.packages.values():
        for klass in package.classes.values():
            method_invocations[klass.name] = {}
            for method in klass.methods.values():
                if method.name in method_invocations.keys():
                    method_invocations[klass.name][method.name].extend(method.method_invocations)
                else:
                    method_invocations[klass.name][method.name] = method.method_invocations

    return method_invocations
