import os
import shutil
import cmd

# Setup Game Directory
NETWORK_ROOT = "NetworkRoot"
if not os.path.exists(NETWORK_ROOT):
    os.makedirs(NETWORK_ROOT)

class NetworkWarsCLI(cmd.Cmd):
    intro = "Welcome to Network Wars! Type help or ? to list commands.\n"
    prompt = "(NetworkWars) "
    
    def do_create_bot(self, bot_name):
        """Create a new AI bot."""
        bot_path = os.path.join(NETWORK_ROOT, f"{bot_name}.py")
        if os.path.exists(bot_path):
            print(f"Bot {bot_name} already exists.")
        else:
            with open(bot_path, 'w') as bot_file:
                bot_file.write("# AI Bot script\n")
            print(f"Bot {bot_name} created successfully.")

    def do_list_bots(self, _):
        """List all AI bots."""
        bots = [f for f in os.listdir(NETWORK_ROOT) if f.endswith('.py')]
        if not bots:
            print("No bots available.")
        else:
            print("Available bots:")
            for bot in bots:
                print(f"- {bot}")

    def do_delete_bot(self, bot_name):
        """Delete an AI bot."""
        bot_path = os.path.join(NETWORK_ROOT, f"{bot_name}.py")
        if os.path.exists(bot_path):
            os.remove(bot_path)
            print(f"Bot {bot_name} deleted successfully.")
        else:
            print(f"Bot {bot_name} does not exist.")

    def do_sandbox(self, bot_name):
        """Test an AI bot in sandbox mode."""
        bot_path = os.path.join(NETWORK_ROOT, f"{bot_name}.py")
        if os.path.exists(bot_path):
            # Placeholder for sandbox mode testing logic
            print(f"Testing {bot_name} in sandbox mode...")
            # Load and execute bot script here
        else:
            print(f"Bot {bot_name} does not exist.")
    
    def do_compete(self, bot_name):
        """Enter a bot into a competitive tournament."""
        bot_path = os.path.join(NETWORK_ROOT, f"{bot_name}.py")
        if os.path.exists(bot_path):
            # Placeholder for competitive mode logic
            print(f"Entering {bot_name} into a tournament...")
            # Load and execute bot script here
        else:
            print(f"Bot {bot_name} does not exist.")

    def do_exit(self, _):
        """Exit the game."""
        print("Thank you for playing Network Wars!")
        return True

if __name__ == '__main__':
    NetworkWarsCLI().cmdloop()
