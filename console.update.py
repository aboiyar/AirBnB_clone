#!/usr/bin/python3
""" Holberton AirBnB Console """
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ General Class for HBNBCommand """
    prompt = '(hbnb) '
    classes = {'BaseModel': BaseModel, 'User': User, 'City': City,
               'Place': Place, 'Amenity': Amenity, 'Review': Review,
               'State': State}

    def do_quit(self, arg):
        """ Exit method for quit typing """
        exit()

    def do_EOF(self, arg):
        """ Exit method for EOF """
        print('')
        exit()

    def emptyline(self):
        """ Method to pass when emptyline entered """
        pass

    def do_create(self, arg):
        """ Create a new instance """
        if len(arg) == 0:
            print('** class name missing **')
            return
        if arg in self.classes:
            new_instance = self.classes[arg]()
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """ Method to print instance """
        args = arg.split()
        if not args:
            print('** class name missing **')
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print('** instance id missing **')
            return
        key = f"{args[0]}.{args[1]}"
        obj = storage.all().get(key)
        if obj:
            print(obj)
        else:
            print('** no instance found **')

    def do_destroy(self, arg):
        """ Method to delete instance with class and id """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print('** instance id missing **')
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print('** no instance found **')

    def do_update(self, arg):
        """ Update an instance with a new attribute """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print('** instance id missing **')
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print('** no instance found **')
            return
        if len(args) == 2:
            print('** attribute name missing **')
            return
        if len(args) == 3:
            print('** value missing **')
            return

        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3].strip("\"'")
        try:
            attr_value = eval(attr_value)
        except (SyntaxError, NameError):
            pass
        setattr(obj, attr_name, attr_value)
        obj.save()

    def default(self, line):
        """ Default method for unknown commands """
        if '.' in line:
            class_name, method_call = line.split('.', 1)
            if class_name in self.classes:
                if method_call.startswith("show(") and method_call.endswith(")"):
                    instance_id = method_call[5:-1].strip("\"'")
                    self.do_show(f"{class_name} {instance_id}")
                elif method_call.startswith("destroy(") and method_call.endswith(")"):
                    instance_id = method_call[8:-1].strip("\"'")
                    self.do_destroy(f"{class_name} {instance_id}")
                elif method_call.startswith("update(") and method_call.endswith(")"):
                    params = method_call[7:-1].split(", ")
                    if len(params) == 3:
                        instance_id = params[0].strip("\"'")
                        attr_name = params[1].strip("\"'")
                        attr_value = params[2]
                        self.do_update(f"{class_name} {instance_id} {attr_name} {attr_value}")
                    else:
                        print("** invalid command **")
                elif method_call == "all()":
                    self.do_all(class_name)
                elif method_call == "count()":
                    self.do_count(class_name)
                else:
                    print("** invalid command **")
            else:
                print("** class doesn't exist **")
        else:
            print("** invalid command **")

    def do_count(self, class_name):
        """ Count instances of a class """
        count = sum(1 for key in storage.all() if key.startswith(class_name + '.'))
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
