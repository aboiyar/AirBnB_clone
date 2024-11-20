#!/usr/bin/python3
"""Unittests for console.py"""
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Unit tests for the HBNBCommand interpreter"""

    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()

    def tearDown(self):
        """Clean up test environment"""
        storage.reload()

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("quit")
            self.assertEqual(f.getvalue(), "")

    def test_EOF(self):
        """Test EOF command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("EOF")
            self.assertEqual(f.getvalue(), "\n")

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("")
            self.assertEqual(f.getvalue(), "")

    def test_create_missing_class(self):
        """Test create command with no class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_create_invalid_class(self):
        """Test create command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_create_valid_class(self):
        """Test create command with valid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            new_id = f.getvalue().strip()
            key = f"BaseModel.{new_id}"
            self.assertIn(key, storage.all())

    def test_show_missing_class(self):
        """Test show command with no class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_show_invalid_class(self):
        """Test show command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_show_missing_id(self):
        """Test show command with no ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_show_instance_not_found(self):
        """Test show command with non-existent ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("show BaseModel 1234-5678")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_show_valid_instance(self):
        """Test show command with valid class name and ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            new_id = f.getvalue().strip()
            key = f"User.{new_id}"
            self.assertIn(key, storage.all())
            self.console.onecmd(f"show User {new_id}")
            self.assertIn(new_id, f.getvalue())

    def test_destroy_missing_class(self):
        """Test destroy command with no class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_destroy_invalid_class(self):
        """Test destroy command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_destroy_missing_id(self):
        """Test destroy command with no ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_destroy_instance_not_found(self):
        """Test destroy command with non-existent ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("destroy BaseModel 1234-5678")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_destroy_valid_instance(self):
        """Test destroy command with valid class name and ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            new_id = f.getvalue().strip()
            key = f"User.{new_id}"
            self.assertIn(key, storage.all())
            self.console.onecmd(f"destroy User {new_id}")
            self.assertNotIn(key, storage.all())

    def test_all_no_class(self):
        """Test all command with no class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            self.assertIn("[", f.getvalue())

    def test_all_invalid_class(self):
        """Test all command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_all_valid_class(self):
        """Test all command with valid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            new_id = f.getvalue().strip()
            self.console.onecmd("all User")
            self.assertIn(new_id, f.getvalue())

    def test_update_missing_class(self):
        """Test update command with no class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_update_invalid_class(self):
        """Test update command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_update_missing_id(self):
        """Test update command with no ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel")
            self.assertEqual(f.getvalue().strip(), "** instance id missing **")

    def test_update_instance_not_found(self):
        """Test update command with non-existent ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("update BaseModel 1234-5678")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_update_valid_instance(self):
        """Test update command with valid class name and ID"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            new_id = f.getvalue().strip()
            self.console.onecmd(f"update User {new_id} name 'John'")
            obj = storage.all()[f"User.{new_id}"]
            self.assertEqual(obj.name, 'John')

    def test_update_with_dict(self):
        """Test update command with dictionary"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create User")
            new_id = f.getvalue().strip()
            self.console.onecmd(f"update User {new_id} {{'age': 30, 'city': 'Lagos'}}")
            obj = storage.all()[f"User.{new_id}"]
            self.assertEqual(obj.age, 30)
            self.assertEqual(obj.city, 'Lagos')


if __name__ == "__main__":
    unittest.main()
