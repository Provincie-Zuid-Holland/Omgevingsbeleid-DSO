<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                version="2.0"><!--Implementers: please note that overriding process-prolog or process-root is 
    the preferred method for meta-stylesheets to use where possible. -->
   <xsl:param name="archiveDirParameter"/>
   <xsl:param name="archiveNameParameter"/>
   <xsl:param name="fileNameParameter"/>
   <xsl:param name="fileDirParameter"/>
   <xsl:variable name="document-uri">
      <xsl:value-of select="document-uri(/)"/>
   </xsl:variable>
   <!--PHASES-->
   <!--PROLOG-->
   <!--XSD TYPES FOR XSLT2-->
   <!--KEYS AND FUNCTIONS-->
   <!--DEFAULT RULES-->
   <!--MODE: SCHEMATRON-SELECT-FULL-PATH-->
   <!--This mode can be used to generate an ugly though full XPath for locators-->
   <xsl:template match="*" mode="schematron-select-full-path">
      <xsl:apply-templates select="." mode="schematron-get-full-path"/>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-->
   <!--This mode can be used to generate an ugly though full XPath for locators-->
   <xsl:template match="*" mode="schematron-get-full-path">
      <xsl:apply-templates select="parent::*" mode="schematron-get-full-path"/>
      <xsl:text>/</xsl:text>
      <xsl:choose>
         <xsl:when test="namespace-uri()=''">
            <xsl:value-of select="name()"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:text>*:</xsl:text>
            <xsl:value-of select="local-name()"/>
            <xsl:text>[namespace-uri()='</xsl:text>
            <xsl:value-of select="namespace-uri()"/>
            <xsl:text>']</xsl:text>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="preceding"
                    select="count(preceding-sibling::*[local-name()=local-name(current())                                   and namespace-uri() = namespace-uri(current())])"/>
      <xsl:text>[</xsl:text>
      <xsl:value-of select="1+ $preceding"/>
      <xsl:text>]</xsl:text>
   </xsl:template>
   <xsl:template match="@*" mode="schematron-get-full-path">
      <xsl:apply-templates select="parent::*" mode="schematron-get-full-path"/>
      <xsl:text>/</xsl:text>
      <xsl:choose>
         <xsl:when test="namespace-uri()=''">@<xsl:value-of select="name()"/>
         </xsl:when>
         <xsl:otherwise>
            <xsl:text>@*[local-name()='</xsl:text>
            <xsl:value-of select="local-name()"/>
            <xsl:text>' and namespace-uri()='</xsl:text>
            <xsl:value-of select="namespace-uri()"/>
            <xsl:text>']</xsl:text>
         </xsl:otherwise>
      </xsl:choose>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-2-->
   <!--This mode can be used to generate prefixed XPath for humans-->
   <xsl:template match="node() | @*" mode="schematron-get-full-path-2">
      <xsl:for-each select="ancestor-or-self::*">
         <xsl:text>/</xsl:text>
         <xsl:value-of select="name(.)"/>
         <xsl:if test="preceding-sibling::*[name(.)=name(current())]">
            <xsl:text>[</xsl:text>
            <xsl:value-of select="count(preceding-sibling::*[name(.)=name(current())])+1"/>
            <xsl:text>]</xsl:text>
         </xsl:if>
      </xsl:for-each>
      <xsl:if test="not(self::*)">
         <xsl:text/>/@<xsl:value-of select="name(.)"/>
      </xsl:if>
   </xsl:template>
   <!--MODE: SCHEMATRON-FULL-PATH-3-->
   <!--This mode can be used to generate prefixed XPath for humans 
	(Top-level element has index)-->
   <xsl:template match="node() | @*" mode="schematron-get-full-path-3">
      <xsl:for-each select="ancestor-or-self::*">
         <xsl:text>/</xsl:text>
         <xsl:value-of select="name(.)"/>
         <xsl:if test="parent::*">
            <xsl:text>[</xsl:text>
            <xsl:value-of select="count(preceding-sibling::*[name(.)=name(current())])+1"/>
            <xsl:text>]</xsl:text>
         </xsl:if>
      </xsl:for-each>
      <xsl:if test="not(self::*)">
         <xsl:text/>/@<xsl:value-of select="name(.)"/>
      </xsl:if>
   </xsl:template>
   <!--MODE: GENERATE-ID-FROM-PATH -->
   <xsl:template match="/" mode="generate-id-from-path"/>
   <xsl:template match="text()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.text-', 1+count(preceding-sibling::text()), '-')"/>
   </xsl:template>
   <xsl:template match="comment()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.comment-', 1+count(preceding-sibling::comment()), '-')"/>
   </xsl:template>
   <xsl:template match="processing-instruction()" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.processing-instruction-', 1+count(preceding-sibling::processing-instruction()), '-')"/>
   </xsl:template>
   <xsl:template match="@*" mode="generate-id-from-path">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:value-of select="concat('.@', name())"/>
   </xsl:template>
   <xsl:template match="*" mode="generate-id-from-path" priority="-0.5">
      <xsl:apply-templates select="parent::*" mode="generate-id-from-path"/>
      <xsl:text>.</xsl:text>
      <xsl:value-of select="concat('.',name(),'-',1+count(preceding-sibling::*[name()=name(current())]),'-')"/>
   </xsl:template>
   <!--MODE: GENERATE-ID-2 -->
   <xsl:template match="/" mode="generate-id-2">U</xsl:template>
   <xsl:template match="*" mode="generate-id-2" priority="2">
      <xsl:text>U</xsl:text>
      <xsl:number level="multiple" count="*"/>
   </xsl:template>
   <xsl:template match="node()" mode="generate-id-2">
      <xsl:text>U.</xsl:text>
      <xsl:number level="multiple" count="*"/>
      <xsl:text>n</xsl:text>
      <xsl:number count="node()"/>
   </xsl:template>
   <xsl:template match="@*" mode="generate-id-2">
      <xsl:text>U.</xsl:text>
      <xsl:number level="multiple" count="*"/>
      <xsl:text>_</xsl:text>
      <xsl:value-of select="string-length(local-name(.))"/>
      <xsl:text>_</xsl:text>
      <xsl:value-of select="translate(name(),':','.')"/>
   </xsl:template>
   <!--Strip characters-->
   <xsl:template match="text()" priority="-1"/>
   <!--SCHEMA SETUP-->
   <xsl:template match="/">
      <xsl:apply-templates select="/" mode="M4"/>
      <xsl:apply-templates select="/" mode="M5"/>
      <xsl:apply-templates select="/" mode="M6"/>
      <xsl:apply-templates select="/" mode="M7"/>
      <xsl:apply-templates select="/" mode="M8"/>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN sch_data_012data:instrumentVersie moet expressionID (AKN/act) zijn-->
   <!--RULE -->
   <xsl:template match="data:BeoogdeRegeling" priority="1000" mode="M4">
      <xsl:variable name="instrument"
                    select="concat(data:instrument/string(), data:instrumentVersie/string())"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches($instrument, '^/akn/(nl|aw|cw|sx)/act')"/>
         <xsl:otherwise>
        {"code": "STOP1026", "ID": "<xsl:text/>
            <xsl:value-of select="$instrument"/>
            <xsl:text/>", "melding": "De waarde van instrument(Versie) <xsl:text/>
            <xsl:value-of select="$instrument"/>
            <xsl:text/> in BeoogdeRegeling MOET een expressionID (/akn/nl/act) zijn", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M4"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M4"/>
   <xsl:template match="@*|node()" priority="-2" mode="M4">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M4"/>
   </xsl:template>
   <!--PATTERN sch_data_013data:instrumentVersie moet JOIN/regdata zijn-->
   <!--RULE -->
   <xsl:template match="data:BeoogdInformatieobject" priority="1000" mode="M5">
      <xsl:variable name="instrument"
                    select="concat(data:instrument/string(), data:instrumentVersie/string())"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches($instrument, '^/join/id/regdata/') or matches($instrument, '^/join/id/pubdata/')"/>
         <xsl:otherwise>
        {"code": "STOP1027", "ID": "<xsl:text/>
            <xsl:value-of select="$instrument"/>
            <xsl:text/>", "melding": "De waarde van instrument(Versie) in BeoogdInformatieobject <xsl:text/>
            <xsl:value-of select="$instrument"/>
            <xsl:text/> MOET een /join/id/regdata zijn", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M5"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M5"/>
   <xsl:template match="@*|node()" priority="-2" mode="M5">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M5"/>
   </xsl:template>
   <!--PATTERN sch_data_014data:Intrekking/data:instrument moet een Work-Id ('/AKN/act/...' of
      '/join/id/regdata/...') hebben-->
   <!--RULE -->
   <xsl:template match="data:Intrekking" priority="1000" mode="M6">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(./data:instrument/string(), '^/akn/(nl|aw|cw|sx)/act|^/join/id/regdata/')"/>
         <xsl:otherwise>
        {"code": "STOP1028", "ID": "<xsl:text/>
            <xsl:value-of select="./data:instrument/string()"/>
            <xsl:text/>", "melding": "Het instrument binnen een Intrekking <xsl:text/>
            <xsl:value-of select="./data:instrument/string()"/>
            <xsl:text/> heeft geen juiste identificatie ('/akn/nl/act/[...]' of '/join/id/regdata/[...]'). Pas de identificatie aan.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M6"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M6"/>
   <xsl:template match="@*|node()" priority="-2" mode="M6">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M6"/>
   </xsl:template>
   <!--PATTERN sch_data_015Een doel kan maar 1 datum juridischWerkendVanaf hebben-->
   <!--RULE -->
   <xsl:template match="data:Tijdstempels" priority="1000" mode="M7">
      <xsl:variable name="Dubbel">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="data:Tijdstempel/data:doel[(../data:soortTijdstempel = 'juridischWerkendVanaf')]">
            <xsl:sort select="data:doel"/>
            <xsl:if test="preceding::data:doel[1] = .">
               <dubbel>
                  <xsl:value-of select="."/>
               </dubbel>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="melding">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$Dubbel/dubbel">
            <xsl:value-of select="."/>
            <xsl:if test="not(position()=last())">
               <xsl:text>; </xsl:text>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(./data:Tijdstempel/data:doel[(../data:soortTijdstempel = 'juridischWerkendVanaf')]) = count(distinct-values(./data:Tijdstempel/data:doel[(../data:soortTijdstempel = 'juridischWerkendVanaf')]))"/>
         <xsl:otherwise>
        {"code": "STOP1077", "Dubbel": "<xsl:text/>
            <xsl:value-of select="$melding"/>
            <xsl:text/>", "melding": "Meer dan één datum juridischWerkendVanaf komt voor bij <xsl:text/>
            <xsl:value-of select="$melding"/>
            <xsl:text/>. Een doel kan maar één datum juridischWerkendVanaf hebben. Verwijder de dubbele datum of wijzig het soortTijdstempel.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M7"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M7"/>
   <xsl:template match="@*|node()" priority="-2" mode="M7">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M7"/>
   </xsl:template>
   <!--PATTERN sch_data_1078Een doel kan maar 1 datum geldigVanaf hebben-->
   <!--RULE -->
   <xsl:template match="data:Tijdstempels" priority="1000" mode="M8">
      <xsl:variable name="Dubbel">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="data:Tijdstempel/data:doel[(../data:soortTijdstempel = 'geldigVanaf')]">
            <xsl:sort select="data:doel"/>
            <xsl:if test="preceding::data:doel[1] = .">
               <dubbel>
                  <xsl:value-of select="."/>
               </dubbel>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="melding">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$Dubbel/dubbel">
            <xsl:value-of select="."/>
            <xsl:if test="not(position()=last())">
               <xsl:text>; </xsl:text>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(./data:Tijdstempel/data:doel[(../data:soortTijdstempel = 'geldigVanaf')]) = count(distinct-values(./data:Tijdstempel/data:doel[(../data:soortTijdstempel = 'geldigVanaf')]))"/>
         <xsl:otherwise>
        {"code": "STOP1078", "Dubbel": "<xsl:text/>
            <xsl:value-of select="$melding"/>
            <xsl:text/>", "melding": "Meer dan één datum geldigVanaf komt voor bij <xsl:text/>
            <xsl:value-of select="$melding"/>
            <xsl:text/>. Een doel kan maar één datum geldigVanaf hebben. Verwijder de dubbele datum of wijzig het soortTijdstempel.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M8"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M8"/>
   <xsl:template match="@*|node()" priority="-2" mode="M8">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M8"/>
   </xsl:template>
</xsl:stylesheet>
