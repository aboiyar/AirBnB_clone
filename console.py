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

    def precmd(self, line):
        """Intercepts commands for special syntax handling"""
        if '.' in line and '(' in line and ')' in line:
            parts = line.split('.')
            class_name = parts[0]
            method_part = parts[1].split('(')
            command = method_part[0]
            args = method_part[1].rstrip(')')
            line = f"{command} {class_name} {args}"
        return line

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
        """Retrieve an instance based on its ID"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy an instance based on its ID"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Retrieve all instances or instances of a specific class"""
        if len(arg) == 0:
            print([str(obj) for obj in storage.all().values()])
        elif arg in self.classes:
            print([str(obj) for key, obj in storage.all().items() if key.startswith(arg)])
        else:
            print("** class doesn't exist **")

    def do_count(self, arg):
        """Retrieve the number of instances of a class"""
        if arg in self.classes:
            count = len([key for key in storage.all() if key.startswith(arg)])
            print(count)
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Update an instance based on its ID"""
        args = arg.split(", ")
        if len(args) < 2:
            print("** class name missing **")
            return
        class_name, id = args[0].split()
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        key = f"{class_name}.{id}"
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attribute_name = args[1]
        attribute_value = args[2]
        instance = storage.all()[key]
        setattr(instance, attribute_name, attribute_value.strip('"'))
        instance.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
