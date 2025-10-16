import json
import os
import sys
import time
import threading

SAVE_DIR = "/Users/Serhii/Documents/Small projects/Pet programm/pet_data" # here enter dir you want this program save file to be
FILE_PATH = os.path.join(SAVE_DIR, "pet_data.json")
os.makedirs(SAVE_DIR, exist_ok=True)

class Pet:
  def __init__(self, name=None, hunger=100, happiness=100, energy=100):
      self.name = name
      self.hunger = hunger
      self.happiness = happiness
      self.energy = energy

      self.file_path = FILE_PATH

      self.interact = self.Interact(self)
      
  def load_data(self):
      if os.path.isfile(self.file_path) and os.path.getsize(self.file_path) > 0:
          with open(self.file_path, 'r') as file:
              return json.load(file)
      return {"pets": {}}

  def save_data(self, data):
      with open(self.file_path, 'w') as file:
          json.dump(data, file, indent=4)

  def create_pet(self):
      pet_data = self.load_data()

      if self.name in pet_data["pets"]:
          print(f"Pet with name '{self.name}' already exists!")
          return

      pet_data["pets"][self.name] = {
          "hunger": self.hunger,
          "happiness": self.happiness,
          "energy": self.energy
      }
      self.save_data(pet_data)
      print(f"[LOG] Записую дані у файл: {os.path.abspath(self.file_path)}")
  def status(self): 
    if self.exists_check(): 
      pet_data = self.load_data()
      print(
          f"\nGood boy's name is: {self.name}\n"
          f"His hunger is: {pet_data['pets'][self.name]['hunger']}\n"
          f"His happiness is: {pet_data['pets'][self.name]['happiness']}\n"
          f"His energy is: {pet_data['pets'][self.name]['energy']}\n"
      )
  def show_pets(self):
    pet_data = self.load_data() 
    counter = 0 
    for pet in pet_data["pets"]: 
      counter += 1 
      print(f"{counter}. {pet}") 
  def get_pets(self):
    pet_data = self.load_data()  
    counter = 0 
    pets = {} 
    for pet in pet_data["pets"]: 
      counter += 1 
      pets[str(counter)] = pet
    return pets

  def exists_check(self):
      pet_data = self.load_data()
      return self.name in pet_data["pets"]

  class Interact:
    def __init__(self, pet):
        self.pet = pet

    def feed(self):
        pet_data = self.pet.load_data()
        if self.pet.name not in pet_data["pets"]:
            print(f"Pet '{self.pet.name}' doesn't exist!")
            return

        if pet_data["pets"][self.pet.name]["hunger"] < 100:
            pet_data["pets"][self.pet.name]["hunger"] += 10
            pet_data["pets"][self.pet.name]["hunger"] = min(100, pet_data["pets"][self.pet.name]["hunger"])
            print(f"{self.pet.name} is fed!")
        else:
            print(f"{self.pet.name} is not hungry!")

        self.pet.save_data(pet_data)

    def play(self):
        pet_data = self.pet.load_data()
        if self.pet.name not in pet_data["pets"]:
            print(f"Pet '{self.pet.name}' doesn't exist!")
            return

        if pet_data["pets"][self.pet.name]["happiness"] < 100:
            pet_data["pets"][self.pet.name]["happiness"] += 10
            pet_data["pets"][self.pet.name]["happiness"] = min(100, pet_data["pets"][self.pet.name]["happiness"])
            print(f"{self.pet.name} is happier!")
        else:
            print(f"{self.pet.name} doesn't want to play!")

        self.pet.save_data(pet_data)
    def sleep(self):
        pet_data = self.pet.load_data()
        if self.pet.name not in pet_data["pets"]:
            print(f"Pet '{self.pet.name}' doesn't exist!")
            return

        if pet_data["pets"][self.pet.name]["energy"] < 100:
            pet_data["pets"][self.pet.name]["energy"] += 10
            pet_data["pets"][self.pet.name]["energy"] = min(100, pet_data["pets"][self.pet.name]["energy"])
            print(f"{self.pet.name} is energized!")
        else:
            print(f"{self.pet.name} doesn't want to play!")
              
        self.pet.save_data(pet_data)

def start_background_thread(file_path):
    def decrease_pet_stats():
      while True:
        time.sleep(15)
        if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
          with open(file_path, 'r') as f:
            pet_data = json.load(f)
          for pet_name, stats in pet_data["pets"].items():
            for stat, value in stats.items():
              pet_data["pets"][pet_name][stat] = max(0, value - 1)
          with open(file_path, 'w') as f:
            json.dump(pet_data, f, indent=4)

    t = threading.Thread(target=decrease_pet_stats, daemon=True)
    t.start()    

def main():
  
  def choose_pet():
    pet = Pet()
    pet.show_pets()
    pets = pet.get_pets()
    chosen_pet_number = input("Enter pet number: ")
    try:
      if chosen_pet_number in pets:
          chosen_pet = pets[chosen_pet_number]
          pet = Pet(chosen_pet)
          return pet
      else:
        print("Invalid input, start again")
        chosen_pet = choose_pet()
        game(chosen_pet)
    except ValueError as e:
      print(f"An error occurred: {e}")
  
  
  def game(pet) -> Pet:
    while True:
      starting_message = "\n1. Creare new pet \n2. Play with your pet \n3. Feed your pet \n4. Let your pet sleep \n5. Show status\n6. Choose your pet \n7. Exit\n"
      print(f"Your pet now is {pet.name}")
      user_input = input(f"{starting_message}\nEnter here: ")
      if user_input == '1':
        pet_name = input("Enter your pet name: ")
        new_pet = Pet(pet_name)
        new_pet.create_pet()
      elif user_input == '2':
        pet.interact.play()
      elif user_input == '3':
        pet.interact.feed()
      elif user_input == '4':
        pet.interact.sleep()
      elif user_input == '5':
        pet.status()
      elif user_input == '6':
        pet = choose_pet()
      elif user_input == '7':
        sys.exit()
      else:
        print("Invalid input, start again")
    
  
  start_game_input = input("1. Create your own pet\n2. Choose from existing\nEnter here: ")
  if start_game_input == '1':
    pet_name = input("Enter your pet name: ")
    pet = Pet(pet_name)
    pet.create_pet()
    game(pet)
  elif start_game_input == '2':
    pet = choose_pet()
    game(pet)
  else:
    print("Invalid input, start again")
    main()

if __name__ == "__main__":
    file_path = FILE_PATH
    start_background_thread(file_path)
    main()