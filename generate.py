# RSquirrel docs generation script
# ( idk what Im doing )
import os
import shutil
import re
import json
import datetime
import urllib.parse

# Folder containing mods
modsFolder = "mods/"
# Folder to save docs into
docsFolder = "docs/"



def CreateDocsForScript( _path, _script, _mod ):
	script = open( os.path.join( _path, _script ), "r" ).read()
	docs = open( os.path.join( docsFolder,_mod + "_scripts.md" ), "a" )

	if docs.tell() == 0:
		docs.write( "# " + _mod + " - Scripts\n" )
		docs.write( "[Go back](./docs_index.md)\n\n" )

	docs.write( "\n## " + _script + "\n\n" )


	# Create a list of functions
	_funcs = []
	for func in re.finditer( "((.{1,}\s{1,}|)function\s{1,}\w{1,}(\ {1,}|\t{1,}|)\(.{0,}\))", script ):
		_funcs.append( script[func.start():func.end()] )

	funcs = []
	# Filter out only the global ones
	if script.find( "globalize_all_functions" ) == -1:
		for func in _funcs:
			reName = re.search( "((?<=(function))\s{1,}\w{1,})", func )
			name = func[reName.start():reName.end()]
			# Regex shortcomings
			name = name.replace( " ", "" )
			name = name.replace( "\t", "" )
			if re.search( "(global\s{1,}function\s{1,}" + name + ")", script ) is not None:
				funcs.append(func)
				#print(name)
	else:
		funcs = _funcs[:]

	_funcs.clear()

	# Remove duplicates
	for func in funcs:
		if func not in _funcs:
			_funcs.append( func )


	for func in _funcs:
		docs.write( "#### `" + func + "`\n" )
		desc = re.search( "(/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/)(?=(\s{1,}" + func[:func.find("(")] + "))", script )
		if desc is not None:
			desc = script[desc.start():desc.end()]
			# Cleanup
			desc = desc.replace("/**", "")
			desc = desc.replace("*/", "")
			desc = desc.replace(" * ", "")
			# No params
			if desc.find("@param") == -1:
				docs.write(desc)
			else:
				docs.write(desc[:desc.find("@param")])
				desc = desc[desc.find("@param"):]
				docs.write( "##### Argumets:\n" )
				while True:
					param = re.search("(?<=@param)(\s{1,}\w{1,})", desc)
					param = param[0]
					param = param.replace( " ", "" )
					param = param.replace( "\t", "" )
					desc = desc[7 + len(param):]
					docs.write( "- `" + param + "`" + desc[:desc.find("@param")])
					desc = desc[desc.find("@param"):]

					if desc.find("@param") == -1:
						docs.write(desc)
						break



		docs.write( "\n" )


def CreateDocsForConvar( _convar, _mod ):
	docs = open( os.path.join( docsFolder,_mod + "_convars.md" ), "a" )

	if docs.tell() == 0:
		docs.write( "# " + _mod + " - ConVars\n" )
		docs.write( "[Go back](./docs_index.md)\n\n" )

	docs.write( "#### `" + _convar["Name"] + "`\n" )
	if "DefaultValue" in _convar:
		docs.write( "**DefaultValue:** `\"" + _convar["DefaultValue"] + "\"`\n")
	if "Description" in _convar:
		docs.write( "  " + _convar["Description"] + "\n" )
	docs.write( "\n")



def main():
	if os.path.exists(docsFolder):
		shutil.rmtree(docsFolder)

	os.mkdir( docsFolder )

	docsIndex = open( os.path.join( docsFolder, "docs_index.md" ), "w" )

	# Populate docs index
	docsIndex.write( "# Documentation index\n" )
	currentTime = datetime.datetime.now()
	docsIndex.write( "> Generated at: {}/{:0>2}/{:0>2} - {:0>2}:{:0>2} (YYYY/MM/DD - HH:MM)\n\n".format( currentTime.year, currentTime.month, currentTime.day, currentTime.hour, currentTime.minute ) )

	docsIndex.write( "### Index:\n" )
	# Loop through all mods
	for mod in os.listdir( modsFolder ):
		# Load mod.json
		modJson = json.loads( open( os.path.join( modsFolder, mod, "mod.json" ) ).read() )
		docsIndex.write( "- **" + modJson["Name"] + "**\n" )

		if "ConVars" in modJson and modJson["ConVars"]:
			docsIndex.write( "  - [ConVars](./" + urllib.parse.quote(modJson["Name"]) + "_convars.md)\n" )
			for convar in modJson["ConVars"]:
				CreateDocsForConvar( convar, modJson["Name"] )

		if "Scripts" in modJson and modJson["Scripts"]:
			docsIndex.write( "  - [Functions](./" + urllib.parse.quote(modJson["Name"]) + "_scripts.md)\n" )
			for script in modJson["Scripts"]:
				CreateDocsForScript( os.path.join( modsFolder, mod, "mod/scripts/vscripts" ), script["Path"], modJson["Name"] )


main()
