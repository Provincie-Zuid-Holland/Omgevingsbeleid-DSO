<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet exclude-result-prefixes="xs" version="2.0"
  xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
  xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
  xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- xlst om geo:Locatie die sinds 1.4.0 een optionele wId kent,
    te ontdoen van dit element. 
    Om een 1.4.0 GIO naar 1.3.0 te converteren.
  -->
  <xsl:output encoding="UTF-8" indent="yes"/>

  <!--
	Vaste parameter voor transformatiescripts: 
	versie waar naar toe getransformeerd wordt
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

  <xsl:template match="geo:Locatie/geo:wId">
    <xsl:comment>1.4.1 element wId verwijderd</xsl:comment>
  </xsl:template>
  
  <xsl:template match="@* | node()">
    <xsl:copy copy-namespaces="no" exclude-result-prefixes="#all">
      <xsl:copy-of select="@*"/>
      <xsl:apply-templates/>
    </xsl:copy>
  </xsl:template>

</xsl:stylesheet>
