from analyzer import *

path = './tests'
files = get_file_names_in_dir(path)
program = get_program(files)
classes = get_classes(program)
class_attrs = get_class_attrs(program)
class_invocations = get_class_invocations(program)
method_invocations = get_method_invocations(program)

print(f'Number of classes is {len(classes)}')

for klass, attr in class_attrs.items():
    print(f"Class {klass} has {len(attr['methods'])} methods and {len(attr['fields'])} fields")

for klass, class_invocation in class_invocations.items():
    print(f"{klass} has {len(class_invocation)} class invocations.")

for klass, method_invocation in method_invocations.items():
    for method, invocations in method_invocation.items():
        print(f"Method {method} in class {klass} has {len(invocations)} method invocations")
