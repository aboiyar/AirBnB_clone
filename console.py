#!/usr/bin/python3
""" Holberton AirBnB Console """
import cmd
import json
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
        """ Update an instance with attributes """
        args = arg.split(' ', 2)
        if len(args) < 1:
            print('** class name missing **')
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print('** instance id missing **')
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print('** no instance found **')
            return
        if len(args) == 2:
            print('** attribute name missing **')
            return

        obj = storage.all()[key]
        try:
            data = json.loads(args[2].replace("'", "\""))
            if isinstance(data, dict):
                for attr_name, attr_value in data.items():
                    setattr(obj, attr_name, attr_value)
                obj.save()
            else:
                print("** invalid dictionary **")
        except json.JSONDecodeError:
            parts = args[2].split()
            if len(parts) == 2:
                attr_name = parts[0]
                attr_value = parts[1].strip("\"'")
                try:
                    attr_value = eval(attr_value)
                except (SyntaxError, NameError):
                    pass
                setattr(obj, attr_name, attr_value)
                obj.save()
            else:
                print('** invalid update format **')

    def default(self, line):
        """ Default method for unknown commands """
        if '.' in line:
            class_name, method_call = line.split('.', 1)
            if class_name in self.classes:
                if method_call.startswith("update(") and method_call.endswith(")"):
                    params = method_call[7:-1].split(", ", 1)
                    instance_id = params[0].strip("\"'")
                    if len(params) > 1 and params[1].startswith("{"):
                        dictionary = params[1]
                        self.do_update(f"{class_name} {instance_id} {dictionary}")
                    elif len(params) > 1:
                        attr_name, attr_value = params[1].split(", ")
                        self.do_update(f"{class_name} {instance_id} {attr_name} {attr_value}")
                    else:
                        print("** invalid command **")
                else:
                    print("** invalid command **")
            else:
                print("** class doesn't exist **")
        else:
            print("** invalid command **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
