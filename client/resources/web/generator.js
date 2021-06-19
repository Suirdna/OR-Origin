let PLUGIN, EVENT, MODE, TARGET, WINNER, START_DATE, END_DATE, START_TIME, END_TIME, STATUS = false, copy, copy_button;

let ORGANIZER_EVENTS = ["Theatre of Blood", "Chambers of Xeric", "Corporeal Beast", "Armadyl", "Bandos", "Saradomin", "Zamorakian", "PK", "Chambers of Xeric Learners", "Hide and Seek", "King Black Dragon", "The Nightmare of Ashihama", "Special"];
let PRE_EVENT = ["tob", "cox", "corp", "arm", "ban", "sar", "zam", "pks", "ler", "hns", "kbd", "nig", "spc"];

let XP_EVENTS = [ "Attack", "Strength", "Defense", "Ranged", "Prayer", "Magic", "Runecrafting",
"Construction", "Hitpoints", "Agility", "Herblore", "Thieving", "Crafting", "Fletching",
"Slayer", "Hunter", "Mining", "Smithing", "Fishing", "Cooking", "Firemaking", "Woodcutting",
"Farming"
];

let PRE_XP_EVENT = ["attack", "strength", "defense", "ranged", "prayer", "magic", "runecrafting",
"construction", "hitpoints", "agility", "herblore", "thieving", "crafting", "fletching",
"slayer", "hunter", "mining", "smithing", "fishing", "cooking", "firemaking", "woodcutting",
"farming"
];
		
let KC_EVENTS = ["Abyssal Sire", "Alchemical Hydra", "Barrows Chests", "Bryophyta", "Callisto",
"Cerberus", "Chambers of Xeric", "Challenge Mode", "Chaos Elemental", "Chaos Fanatic", "Commander Zilyana",
"Corporeal Beast", "Crazy Archaeologist", "Dagannoth Prime", "Dagannoth Rex", "Dagannoth Supreme",
"Deranged Archaeologist", "General Graardor", "Giant Mole", "Grotesque Guardians", "Hespori", "Kalphite Queen",
"King Black Dragon", "Kraken", "Kree'Arra", "K'ril Tsutsaroth", "Mimic", "Nightmare",
"Obor", "Sarachnis", "Scorpia", "Skotizo", "Tempoross" , "The Gauntlet", "The Corrupted Gauntlet", "Theatre of Blood", "Theatre of Blood CM",
"Thermonuclear Smoke Devil", "TzKal-Zuk", "TzTok-Jad", "Venenatis", "Vet'ion", "Vorkath", "Wintertodt",
"Zalcano", "Zulrah"
];

let PRE_KC_EVENT = ["sire", "hydra", "barrows", "bryo", "call", "cerb", "cox", "cm", "chaosele",
"chaosfan", "sara", "corp", "crazyarch", "prime", "rex", "supreme", "derarch", "bandos", "mole",
"gargs", "hespori", "kq", "kbd", "kraken", "arma", "zammy", "mimic", "nm", "obor", "sarachnis",
"scorpia", "skotizo", "temp", "gaunt", "corrugaunt", "tob", "tobcm", "smokedevil", "zuk", "jad", "vene", "vetion",
"vork", "wt", "zalca", "zulrah"
];
	 
function Auto() {
	PLUGIN = document.getElementById("plugin");
	EVENT = document.getElementById("events");
	MODE = document.getElementById("mode");
	TARGET = document.getElementById("target");
	WINNER = document.getElementById("prize_count");
	START_DATE = document.getElementById("start_date");
	END_DATE = document.getElementById("end_date");
	START_TIME = document.getElementById("start_time");
	END_TIME = document.getElementById("end_time");
	copy = document.getElementById("copy_text");
	copy_button = document.getElementById("copy");
}

function checkSafe(){
	safe_color = '2px solid #f4d017'; 
	unsafe_color = '2px solid red';
	STATUS = false;
	
	if (PLUGIN.value == '.add'){
		PLUGIN.style.border = safe_color;
		EVENT.style.border = safe_color;
		MODE.style.border = safe_color;
		TARGET.style.border = safe_color;
		WINNER.style.border = safe_color;
		START_DATE.style.border = unsafe_color;
		END_DATE.style.border = safe_color;
		START_TIME.style.border = unsafe_color;
		END_TIME.style.border = safe_color;
		copy.innerHTML = "COPY";
		copy_button.style = 'background-color: #1d1f22;';
		
		MODE.disabled = true;
		TARGET.disabled = true;
		WINNER.disabled = true;
		END_DATE.disabled = true;
		END_TIME.disabled = true;
		
		if (START_DATE.value != ''){
			START_DATE.style.border = safe_color;
		}else{
			START_DATE.style.border = unsafe_color;
		}
		
		if (START_TIME.value != ''){
			START_TIME.style.border = safe_color;
		}else{
			START_TIME.style.border = unsafe_color;
		}
		
		if (START_DATE.value != '' && START_TIME.value != ''){
			STATUS = true;
		}else{
			STATUS = false;
		}
	}else if(PLUGIN.value == '.addxpevent' || PLUGIN.value == '.addkcevent'){
		PLUGIN.style.border = safe_color;
		EVENT.style.border = safe_color;
		MODE.style.border = unsafe_color;
		TARGET.style.border = unsafe_color;
		WINNER.style.border = unsafe_color;
		START_DATE.style.border = unsafe_color;
		END_DATE.style.border = unsafe_color;
		START_TIME.style.border = unsafe_color;
		END_TIME.style.border = unsafe_color;
		copy.innerHTML = "COPY";
		copy_button.style = 'background-color: #1d1f22;';
		
		MODE.disabled = false;
		TARGET.disabled = false;
		WINNER.disabled = false;
		END_DATE.disabled = false;
		END_TIME.disabled = false;
		
		if (MODE.value != 'mode'){
			MODE.style.border = safe_color;
		}else{
			MODE.style.border = unsafe_color;
			TARGET.value = 'XP / KC';
		}
		
		if(MODE.value == 'standart'){
			MODE.style.border = safe_color;
			TARGET.value = '0';
			TARGET.style.border = safe_color;
			TARGET.disabled = true;
		}
		
		if(MODE.value == 'rush'){
			MODE.style.border = safe_color;
			TARGET.value = '100000';
			TARGET.style.border = safe_color;
			TARGET.disabled = false;
		}
		
		if (WINNER.value != 'winner_count'){
			WINNER.style.border = safe_color;
		}else{
			WINNER.style.border = unsafe_color;
		}
		
		if (START_DATE.value != ''){
			START_DATE.style.border = safe_color;
		}else{
			START_DATE.style.border = unsafe_color;
		}
				
		if (START_TIME.value != ''){
			START_TIME.style.border = safe_color;
		}else{
			START_TIME.style.border = unsafe_color;
		}
		
		if (END_DATE.value != ''){
			END_DATE.style.border = safe_color;
		}else{
			END_DATE.style.border = unsafe_color;
		}
		
		if (END_TIME.value != ''){
			END_TIME.style.border = safe_color;
		}else{
			END_TIME.style.border = unsafe_color;
		}
		
		if (MODE.value != 'mode' && TARGET.value != 'XP / KC' && WINNER.value != 'winner_count' && START_DATE.value != '' && END_DATE.value != '' && START_TIME.value != '' && END_TIME.value != ''){
			STATUS = true;
		}else{
			STATUS = false;
		}
		
	}else {
		PLUGIN.style.border = unsafe_color;
		EVENT.style.border = unsafe_color;
		MODE.style.border = unsafe_color;
		TARGET.style.border = unsafe_color;
		WINNER.style.border = unsafe_color;
		START_DATE.style.border = unsafe_color;
		END_DATE.style.border = unsafe_color;
		START_TIME.style.border = unsafe_color;
		END_TIME.style.border = unsafe_color;
		copy.innerHTML = "COPY";
		copy_button.style = 'background-color: #1d1f22;';
		
		PLUGIN.disabled = false;
		EVENT.disabled = false;
		MODE.disabled = false;
		TARGET.disabled = false;
		WINNER.disabled = false;
		START_DATE.disabled = false;
		END_DATE.disabled = false;
		START_TIME.disabled = false;
		END_TIME.disabled = false;
	}
}

function setPlugin() {
    if (PLUGIN.value == ".add") {
		clear(EVENT);
		for (i = 0; i < ORGANIZER_EVENTS.length; i++) {
			var option = document.createElement("option");
			option.text = ORGANIZER_EVENTS[i];
			EVENT.add(option);
		}
	}else if (PLUGIN.value == ".addxpevent") {
		clear(EVENT);
		for (i = 0; i < XP_EVENTS.length; i++) {
			var option = document.createElement("option");
			option.text = XP_EVENTS[i];
			EVENT.add(option);
		}
	}else if (PLUGIN.value == ".addkcevent") {
		clear(EVENT);
		for (i = 0; i < KC_EVENTS.length; i++) {
			var option = document.createElement("option");
			option.text = KC_EVENTS[i];
			EVENT.add(option);
		}
	}
}

function setMode(MODE, TARGET) {
	if(	MODE.value == "rush"){
		TARGET.disabled = false;
		TARGET.value = 100000;
	}else{
		TARGET.disabled = true;
		TARGET.value = 0;
	}
}

function clear(object){
	object.innerHTML = "";
}

function generateCommand(){
	let plugin_d, event_d, mode_d, target_d, winner_d, start_date_d, end_date_d, start_time_d, end_time_d;
	let EVENTS, EVENTS_PRE;
	let global_text, extra='Additional information.';
	
	if (STATUS == true){
		plugin_d = PLUGIN.value;
		event_d = EVENT.value;
		mode_d = MODE.value;
		target_d = TARGET.value;
		winner_d = WINNER.value;
		start_date_d = START_DATE.value;
		end_date_d = END_DATE.value;
		start_time_d = START_TIME.value;
		end_time_d = END_TIME.value;
		
		if (plugin_d == '.add'){
			start_date_d = start_date_d.substring(5, 10);
			start_time_d = start_time_d.substring(0, 2);
			start_date_d = start_date_d.replace('-', '.');
			for (i = 0; i < ORGANIZER_EVENTS.length; i++) {
				if (ORGANIZER_EVENTS[i] == event_d){
					global_text = `${plugin_d} ${PRE_EVENT[i]} ${start_date_d} ${start_time_d} ${extra}`;
					const command = document.createElement('textarea');
					command.value = global_text;
					document.body.appendChild(command);
					command.select();
					document.execCommand('copy');
					document.body.removeChild(command);
					copy.innerHTML = "COPIED";
					copy_button.style = 'background-color: #f4d017;';
				}
			}
		}
		
		if (plugin_d == '.addxpevent' || PLUGIN.value == '.addkcevent'){
			start_date_d = start_date_d.substring(5, 10);
			start_time_d = start_time_d.substring(0, 2);
			end_date_d = end_date_d.substring(5, 10);
			end_time_d = end_time_d.substring(0, 2);
			start_date_d = start_date_d.replace('-', '.');
			end_date_d = end_date_d.replace('-', '.');
			
			if  (plugin_d == '.addxpevent'){
				EVENTS = XP_EVENTS;
				EVENTS_PRE = PRE_XP_EVENT;
			}else if (plugin_d == '.addkcevent'){
				EVENTS = KC_EVENTS;
				EVENTS_PRE = PRE_KC_EVENT;
			}
			
			for (i = 0; i < EVENTS.length; i++) {
				if (EVENTS[i] == event_d){
					global_text = `${plugin_d} ${target_d} ${EVENTS_PRE[i]} ${winner_d} ${start_date_d} ${end_date_d} ${start_time_d} ${end_time_d} ${extra}`;
					  const command = document.createElement('textarea');
					  command.value = global_text;
					  document.body.appendChild(command);
					  command.select();
					  document.execCommand('copy');
					  document.body.removeChild(command);
					  copy.innerHTML = "COPIED";
					  copy_button.style = 'background-color: #f4d017;';
				}
			}
		}
	}
}
