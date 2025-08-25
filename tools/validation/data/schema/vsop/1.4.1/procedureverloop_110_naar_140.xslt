<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet exclude-result-prefixes="xs" version="2.0"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:data="https://standaarden.overheid.nl/stop/imop/data/">

	<!--
	Versie 1.4.1
	-->
	<xsl:output encoding="UTF-8" indent="yes" />

	<!--
	Vaste parameter voor transformatiescripts: versie waar naar toe getransformeerd wordt
  -->
	<xsl:param as="xs:string" name="schemaversie"/>
	<xsl:template match="/*">
		<xsl:copy>
			<xsl:attribute name="schemaversie">
				<xsl:value-of select="$schemaversie"/>
			</xsl:attribute>
			<xsl:apply-templates select="@*[not(local-name()='schemaversie')]|node()"/>
		</xsl:copy>
	</xsl:template>

	<!--
	  xlst om data:Procedurestap te ontdoen van het optionele veld Actor
    dat in STOP 1.4 niet meer aanwezig is.
  -->
	<xsl:template match="data:actor"/>

	<!--
	  Identiteit-transformatie
  -->
	<xsl:template match="@*|node()">
		<xsl:copy copy-namespaces="no" exclude-result-prefixes="#all">
			<xsl:copy-of select="@*" />
			<xsl:apply-templates />
		</xsl:copy>
	</xsl:template>

</xsl:stylesheet>
