import discord
import random

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)

# List of WMMT-related roasts and jokes
wmmt_roasts = [
    "You brake so early, even the AI thinks you're looking for a parking spot.",
    "Your corner exits are so wide, GPS starts recalculating your route.",
    "The only thing you're consistent at is finding every guardrail on the course.",
    "You handle corners like they're optional.",
    "The only time you’re fast is when you’re pressing yes to challenging guests."
]

wmmt_jokes = [
    "Why do WMMT players never save money? Because every 'just one more run' is worth a week's groceries.",
    "Why did the WMMT player cry after setting a PB? Because it cost them more than their car’s down payment.",
    "Why did the WMMT driver cross the road? Because he missed the turn… again."
]

# List of maps with optimal HP settings for ?vspickmap
maps_with_hp = {
    'C1 Area (In)': [720],
    'C1 Area (Out)': [700],
    'New Belt Line Area (CCW)': [760],
    'New Belt Line Area (CW)': [840],
    'Sub-center (Shibuya/Shinjuku)': [700],
    'Sub-center (Ikebukuro/Yamate Tunnel)': [700],
    'Wangan Area (Eastbound/Westbound)': [840],
    'Yokohane Area (Upward/Downward)': [840],
    'Yaesu Area (Inward/Outward)': [700],
    'Osaka Area': [760],
    'Nagoya Area': [800],
    'Fukuoka Area': [740],
    'Kobe Area': [660],
    'Hiroshima Area': [660],
    'Hakone Area (Inbound/Outbound)': [760],
    'Mt. Taikan Area (Uphill)': [760],
    'Mt. Taikan Area (Downhill)': [740]
}

# HP increment rule: 600 to 800 in increments of 20, then 815, 830, 835, 840
hp_values_increment_rule = list(range(600, 801, 20)) + [815, 830, 835, 840]

@client.event
async def on_ready():
    print(f'Bot {client.user} is now online and ready!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Prevents the bot from responding to itself

    if message.content.startswith('?tournamentbracket'):
        await handle_tournament_bracket_command(message)
    elif message.content.startswith('?vspickmap'):
        await handle_vspickmap_command(message)
    elif message.content.startswith('?roast'):
        await handle_roast_command(message)
    elif message.content.startswith('?joke'):
        await handle_joke_command(message)

async def handle_tournament_bracket_command(message):
    args = message.content.split()
    mentions = message.mentions

    if len(args) == 1:
        response = (
            "Usage of ?tournamentbracket command:\n"
            "`?tournamentbracket standard @User1 @User2 ...` - Creates an elimination bracket."
        )
        await message.channel.send(response)
        return

    if len(mentions) < 2:
        response = "Please mention at least 2 users to create a tournament bracket."
        await message.channel.send(response)
        return

    if args[1].lower() == 'standard':
        response = generate_elimination_bracket(mentions)
    else:
        response = "Invalid argument. Please use `standard`."

    await message.channel.send(response)

async def handle_vspickmap_command(message):
    args = message.content.split()

    if len(args) == 1:
        response = (
            "Usage of ?vspickmap command:\n"
            "`?vspickmap standard` - Picks a map with optimal HP settings.\n"
            "`?vspickmap spicy` - Picks a map and locks HP values to 760 and above following the increment rule.\n"
            "`?vspickmap random` - Picks a map and selects a random HP from 600 and above following the increment rule."
        )
        await message.channel.send(response)
        return

    mode = args[1].lower()
    if mode == 'standard':
        selected_map = random.choice(list(maps_with_hp.keys()))
        hp = maps_with_hp[selected_map][0]  # Standard HP is the first (and only) value
        response = f'Randomly Selected Area: {selected_map}\nOptimal HP: {hp} HP'
    elif mode == 'spicy':
        selected_map = random.choice(list(maps_with_hp.keys()))
        possible_hps = [hp for hp in hp_values_increment_rule if hp >= 760]
        hp = random.choice(possible_hps)
        response = f'Randomly Selected Area: {selected_map}\nSpicy HP: {hp} HP'
    elif mode == 'random':
        selected_map = random.choice(list(maps_with_hp.keys()))
        possible_hps = [hp for hp in hp_values_increment_rule]
        hp = random.choice(possible_hps)
        response = f'Randomly Selected Area: {selected_map}\nRandom HP: {hp} HP'
    else:
        response = "Invalid argument. Please use `standard`, `spicy`, or `random`."

    await message.channel.send(response)

async def handle_roast_command(message):
    roast = random.choice(wmmt_roasts)
    response = f"@{message.author.display_name} {roast}"
    await message.channel.send(response)

async def handle_joke_command(message):
    joke = random.choice(wmmt_jokes)
    await message.channel.send(joke)

def generate_elimination_bracket(mentions):
    """Generates a full elimination tournament bracket."""
    participants = [mention.display_name for mention in mentions]
    random.shuffle(participants)
    rounds = generate_tournament_bracket(participants)
    
    response = "Elimination Tournament Bracket:\n"
    for i, round_matches in enumerate(rounds):
        response += f"\n**Round {i + 1}:**\n"
        for match in round_matches:
            if len(match) == 2:
                response += f"{match[0]} vs {match[1]}\n"
            else:
                response += f"{match[0]} has a bye.\n"

    response += f"\n**Finals:**\n{rounds[-1][0][0]} vs {rounds[-1][0][1]}"
    return response

def generate_tournament_bracket(participants):
    """Generates the full elimination tournament bracket with matches up to the final."""
    rounds = []
    current_round = participants[:]
    
    while len(current_round) > 1:
        round_matches = []
        next_round = []
        
        for i in range(0, len(current_round), 2):
            if i + 1 < len(current_round):
                round_matches.append((current_round[i], current_round[i + 1]))
                next_round.append(random.choice([current_round[i], current_round[i + 1]]))
            else:
                round_matches.append((current_round[i],))
                next_round.append(current_round[i])  # The participant gets a bye

        rounds.append(round_matches)
        current_round = next_round
    
    return rounds

client.run('API_KEY')
