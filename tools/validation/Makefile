DIR ?= ../../output


install-linux-deps:
	apt install libxml2-utils xmlstarlet


download-saxon:
	mkdir saxon-download saxon
	wget -P saxon-download https://github.com/Saxonica/Saxon-HE/releases/download/SaxonHE11-6/SaxonHE11-6J.zip
	unzip saxon-download/SaxonHE11-6J.zip -d saxon


./saxon/saxon-he-11.6.jar: 
	$(MAKE) download-saxon


test: ./saxon/saxon-he-11.6.jar test-xsd test-schematron


test-xsd:
	@python app/cmds.py xsd-all $(DIR)


test-schematron:
	@python app/cmds.py schematron-all $(DIR)


download-geostandaarden-xml:
	wget -r -np -nH --cut-dirs=3 -R "index.html*" -P ./data/schema/geostandaarden https://register.geostandaarden.nl/xmlschema/tpod/v3.1.0/IMOW/
	wget -r -np -nH --cut-dirs=3 -R "index.html*" -P ./data/schema/geostandaarden https://register.geostandaarden.nl/xmlschema/tpod/v3.1.0/bestanden-ow/
	wget -r -np -nH --cut-dirs=3 -R "index.html*" -P ./data/schema/geostandaarden https://register.geostandaarden.nl/xmlschema/tpod/v3.1.0/xlink/


geostandaarden-generate-files:
	@python app/cmds.py geostandaarden-generate-files https://register.geostandaarden.nl/xmlschema/tpod/v3.1.0
