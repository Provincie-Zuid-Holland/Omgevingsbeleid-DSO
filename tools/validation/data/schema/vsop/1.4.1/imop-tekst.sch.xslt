<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:tekst="https://standaarden.overheid.nl/stop/imop/tekst/"
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
   <xsl:key match="tekst:*[@eId]" name="alleEIDsVoorIntRefs" use="@eId"/>
   <xsl:key match="tekst:ExtIoRef[@wId]"
            name="alleExtIoRefVoorIntIoRefs"
            use="@wId"/>
   <xsl:key match="tekst:*[@eId][not(ancestor-or-self::tekst:WijzigInstructies)]"
            name="alleEIDs"
            use="@eId"/>
   <xsl:key match="tekst:*[@wId][not(ancestor-or-self::tekst:WijzigInstructies)]"
            name="alleWIDs"
            use="@wId"/>
   <xsl:key match="tekst:Noot[not(ancestor-or-self::tekst:WijzigInstructies)]"
            name="alleNootIDs"
            use="@id"/>
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
      <xsl:apply-templates select="/" mode="M9"/>
      <xsl:apply-templates select="/" mode="M11"/>
      <xsl:apply-templates select="/" mode="M13"/>
      <xsl:apply-templates select="/" mode="M14"/>
      <xsl:apply-templates select="/" mode="M15"/>
      <xsl:apply-templates select="/" mode="M16"/>
      <xsl:apply-templates select="/" mode="M17"/>
      <xsl:apply-templates select="/" mode="M18"/>
      <xsl:apply-templates select="/" mode="M19"/>
      <xsl:apply-templates select="/" mode="M23"/>
      <xsl:apply-templates select="/" mode="M24"/>
      <xsl:apply-templates select="/" mode="M25"/>
      <xsl:apply-templates select="/" mode="M26"/>
      <xsl:apply-templates select="/" mode="M27"/>
      <xsl:apply-templates select="/" mode="M28"/>
      <xsl:apply-templates select="/" mode="M29"/>
      <xsl:apply-templates select="/" mode="M30"/>
      <xsl:apply-templates select="/" mode="M31"/>
      <xsl:apply-templates select="/" mode="M32"/>
      <xsl:apply-templates select="/" mode="M33"/>
      <xsl:apply-templates select="/" mode="M34"/>
      <xsl:apply-templates select="/" mode="M35"/>
      <xsl:apply-templates select="/" mode="M36"/>
      <xsl:apply-templates select="/" mode="M37"/>
      <xsl:apply-templates select="/" mode="M38"/>
      <xsl:apply-templates select="/" mode="M39"/>
      <xsl:apply-templates select="/" mode="M40"/>
      <xsl:apply-templates select="/" mode="M41"/>
      <xsl:apply-templates select="/" mode="M42"/>
      <xsl:apply-templates select="/" mode="M43"/>
      <xsl:apply-templates select="/" mode="M44"/>
      <xsl:apply-templates select="/" mode="M45"/>
      <xsl:apply-templates select="/" mode="M46"/>
      <xsl:apply-templates select="/" mode="M47"/>
      <xsl:apply-templates select="/" mode="M48"/>
      <xsl:apply-templates select="/" mode="M49"/>
      <xsl:apply-templates select="/" mode="M50"/>
      <xsl:apply-templates select="/" mode="M51"/>
      <xsl:apply-templates select="/" mode="M52"/>
      <xsl:apply-templates select="/" mode="M53"/>
      <xsl:apply-templates select="/" mode="M54"/>
      <xsl:apply-templates select="/" mode="M55"/>
      <xsl:apply-templates select="/" mode="M56"/>
      <xsl:apply-templates select="/" mode="M57"/>
      <xsl:apply-templates select="/" mode="M58"/>
      <xsl:apply-templates select="/" mode="M59"/>
      <xsl:apply-templates select="/" mode="M60"/>
      <xsl:apply-templates select="/" mode="M61"/>
      <xsl:apply-templates select="/" mode="M62"/>
      <xsl:apply-templates select="/" mode="M63"/>
      <xsl:apply-templates select="/" mode="M64"/>
      <xsl:apply-templates select="/" mode="M65"/>
      <xsl:apply-templates select="/" mode="M66"/>
      <xsl:apply-templates select="/" mode="M67"/>
      <xsl:apply-templates select="/" mode="M68"/>
      <xsl:apply-templates select="/" mode="M69"/>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN sch_tekst_001Lijst - Nummering lijstitems-->
   <!--RULE -->
   <xsl:template match="tekst:Lijst[@type = 'ongemarkeerd']"
                 priority="1001"
                 mode="M4">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(tekst:Li/tekst:LiNummer[not(@wijzigactie='verwijder')]) = 0"/>
         <xsl:otherwise>
				{"code": "STOP0001", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "De Lijst met eId <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> van type 'ongemarkeerd' heeft LiNummer-elementen met een nummering of opsommingstekens, dit is niet toegestaan. Pas het type van de lijst aan of verwijder de LiNummer-elementen.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M4"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="tekst:Lijst[@type = 'expliciet']" priority="1000" mode="M4">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(tekst:Li[tekst:LiNummer]) = count(tekst:Li)"/>
         <xsl:otherwise>
				{"code": "STOP0002", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "De Lijst met eId <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> van type 'expliciet' heeft geen LiNummer elementen met nummering of opsommingstekens, het gebruik van LiNummer is verplicht. Pas het type van de lijst aan of voeg LiNummer's met nummering of opsommingstekens toe aan de lijst-items", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M4"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M4"/>
   <xsl:template match="@*|node()" priority="-2" mode="M4">
      <xsl:apply-templates select="*" mode="M4"/>
   </xsl:template>
   <!--PATTERN sch_tekst_022Alinea - Bevat content-->
   <!--RULE -->
   <xsl:template match="tekst:Al" priority="1000" mode="M5">

		<!--REPORT fout-->
      <xsl:if test="normalize-space(./string()) = '' and not(tekst:InlineTekstAfbeelding | tekst:Nootref)">
				{"code": "STOP0005", "element": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/local-name()"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "De alinea voor element <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/local-name()"/>
         <xsl:text/> met id <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/> bevat geen tekst. Verwijder de lege alinea", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M5"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M5"/>
   <xsl:template match="@*|node()" priority="-2" mode="M5">
      <xsl:apply-templates select="*" mode="M5"/>
   </xsl:template>
   <!--PATTERN sch_tekst_027Kop - Bevat content-->
   <!--RULE -->
   <xsl:template match="tekst:Kop" priority="1000" mode="M6">

		<!--REPORT fout-->
      <xsl:if test="normalize-space(./string()) = ''">
				{"code": "STOP0006", "element": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/local-name()"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "De kop voor element <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/local-name()"/>
         <xsl:text/> met id <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/> bevat geen tekst. Corrigeer de kop of verplaats de inhoud naar een ander element", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M6"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M6"/>
   <xsl:template match="@*|node()" priority="-2" mode="M6">
      <xsl:apply-templates select="*" mode="M6"/>
   </xsl:template>
   <!--PATTERN sch_tekst_003Tabel - Referenties naar een noot-->
   <!--RULE -->
   <xsl:template match="tekst:table//tekst:Nootref" priority="1001" mode="M7">
      <xsl:variable name="nootID" select="@refid"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:table//tekst:Noot[@id = $nootID]"/>
         <xsl:otherwise>
				{"code": "STOP0008", "ref": "<xsl:text/>
            <xsl:value-of select="@refid"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/>", "melding": "De referentie naar de noot met id <xsl:text/>
            <xsl:value-of select="@refid"/>
            <xsl:text/> verwijst niet naar een noot in dezelfde tabel <xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/>. Verplaats de noot waarnaar verwezen wordt naar de tabel of vervang de referentie in de tabel voor de noot waarnaar verwezen wordt", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="tekst:Nootref" priority="1000" mode="M7">
      <xsl:variable name="nootID" select="@refid"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:table"/>
         <xsl:otherwise>
				{"code": "STOP0007", "ref": "<xsl:text/>
            <xsl:value-of select="@refid"/>
            <xsl:text/>", "melding": "De referentie naar de noot met id <xsl:text/>
            <xsl:value-of select="@refid"/>
            <xsl:text/> staat niet in een tabel. Vervang de referentie naar de noot voor de noot waarnaar verwezen wordt", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M7"/>
   <xsl:template match="@*|node()" priority="-2" mode="M7">
      <xsl:apply-templates select="*" mode="M7"/>
   </xsl:template>
   <!--PATTERN sch_tekst_004Lijst - plaatsing tabel in een lijst-->
   <!--RULE -->
   <xsl:template match="tekst:Li[tekst:table]" priority="1000" mode="M8">

		<!--REPORT waarschuwing-->
      <xsl:if test="self::tekst:Li/tekst:table and not(ancestor::tekst:Instructie)">
				{"code": "STOP0009", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het lijst-item <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> bevat een tabel, onderzoek of de tabel buiten de lijst kan worden geplaatst, eventueel door de lijst in delen op te splitsen", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M8"/>
   <xsl:template match="@*|node()" priority="-2" mode="M8">
      <xsl:apply-templates select="*" mode="M8"/>
   </xsl:template>
   <!--PATTERN sch_tekst_032Illustratie - attributen kleur en schaal worden niet ondersteund-->
   <!--RULE -->
   <xsl:template match="tekst:Illustratie | tekst:InlineTekstAfbeelding"
                 priority="1000"
                 mode="M9">

		<!--REPORT ontraden-->
      <xsl:if test="@schaal">
				{"code": "STOP0045", "ouder": "<xsl:text/>
         <xsl:value-of select="local-name(ancestor::*[@eId][1])"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="ancestor::*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "De Illustratie binnen <xsl:text/>
         <xsl:value-of select="local-name(ancestor::*[@eId][1])"/>
         <xsl:text/> met eId <xsl:text/>
         <xsl:value-of select="ancestor::*[@eId][1]/@eId"/>
         <xsl:text/> heeft een waarde voor attribuut @schaal. Dit attribuut wordt genegeerd in de publicatie van documenten volgens STOP 1.4.1. In plaats daarvan wordt het attribuut @dpi gebruikt voor de berekening van de afbeeldingsgrootte. Verwijder het attribuut @schaal.", "ernst": "ontraden"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT ontraden-->
      <xsl:if test="@kleur">
				{"code": "STOP0046", "ouder": "<xsl:text/>
         <xsl:value-of select="local-name(ancestor::*[@eId][1])"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="ancestor::*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "De Illustratie binnen <xsl:text/>
         <xsl:value-of select="local-name(ancestor::*[@eId][1])"/>
         <xsl:text/> met eId <xsl:text/>
         <xsl:value-of select="ancestor::*[@eId][1]/@eId"/>
         <xsl:text/> heeft een waarde voor attribuut @kleur. Dit attribuut wordt genegeerd in de publicatie van STOP 1.4.1. Verwijder het attribuut @kleur.", "ernst": "ontraden"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M9"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M9"/>
   <xsl:template match="@*|node()" priority="-2" mode="M9">
      <xsl:apply-templates select="*" mode="M9"/>
   </xsl:template>
   <!--PATTERN sch_tekst_006Referentie intern - correcte verwijzing-->
   <!--RULE -->
   <xsl:template match="tekst:IntRef[not(ancestor::tekst:RegelingMutatie | ancestor::tekst:BesluitMutatie)]"
                 priority="1000"
                 mode="M11">
      <xsl:variable name="doelwit_eid">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with(@ref, '!')">
               <xsl:value-of select="substring-after(@ref, '#')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="@ref"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="doelwit_component">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="starts-with(@ref, '!')">
               <xsl:value-of select="translate(substring-before(@ref, '#'), '!', '')"/>
            </xsl:when>
            <xsl:otherwise>[zonder_component]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="intref_component">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="ancestor::tekst:*[@componentnaam]">
               <xsl:value-of select="ancestor::tekst:*[@componentnaam][1]/@componentnaam"/>
            </xsl:when>
            <xsl:otherwise>[in_hoofdtekst]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="scopeNaam">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="@scope">
               <xsl:value-of select="@scope"/>
            </xsl:when>
            <xsl:otherwise>[geen-scope]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="localName">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="$doelwit_component = '[zonder_component]'">
               <xsl:choose>
                  <xsl:when test="$intref_component = '[in_hoofdtekst]'">
                     <xsl:value-of select="key('alleEIDsVoorIntRefs', $doelwit_eid)[not(ancestor::tekst:*[@componentnaam])]/local-name()"/>
                  </xsl:when>
                  <xsl:otherwise>
                     <xsl:value-of select="key('alleEIDsVoorIntRefs', $doelwit_eid)[ancestor::tekst:*[@componentnaam][1]/@componentnaam = $intref_component]/local-name()"/>
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:when>
            <xsl:when test="$intref_component = '[in_hoofdtekst]'">
               <xsl:value-of select="key('alleEIDsVoorIntRefs', $doelwit_eid)[ancestor::tekst:*[@componentnaam][1]/@componentnaam = $doelwit_component]/local-name()"/>
            </xsl:when>
            <xsl:otherwise/>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="var_component">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="$doelwit_component = '[zonder_component]'">
               <xsl:choose>
                  <xsl:when test="$intref_component = '[in_hoofdtekst]'">in de hoofdtekst</xsl:when>
                  <xsl:otherwise>
                     <xsl:text>in de tekst van component '</xsl:text>
                     <xsl:value-of select="$intref_component"/>
                     <xsl:text>'</xsl:text>
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:when>
            <xsl:otherwise>
               <xsl:text>in component '</xsl:text>
               <xsl:value-of select="$doelwit_component"/>
               <xsl:text>'</xsl:text>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$localName != ''"/>
         <xsl:otherwise>
				{"code": "STOP0010", "ref": "<xsl:text/>
            <xsl:value-of select="@ref"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="$doelwit_eid"/>
            <xsl:text/>", "component": "<xsl:text/>
            <xsl:value-of select="$var_component"/>
            <xsl:text/>", "melding": "Voor de verwijzing tekst:IntRef met @ref=<xsl:text/>
            <xsl:value-of select="@ref"/>
            <xsl:text/> kan geen bijbehorend tekst-element met eId <xsl:text/>
            <xsl:value-of select="$doelwit_eid"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="$var_component"/>
            <xsl:text/> gevonden worden. Controleer de referentie, corrigeer ofwel de referentie ofwel de identificatie van het element waarnaar wordt verwezen.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$localName = '' or $scopeNaam = '[geen-scope]' or $scopeNaam = $localName"/>
         <xsl:otherwise>
				{"code": "STOP0053", "ref": "<xsl:text/>
            <xsl:value-of select="@ref"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="$doelwit_eid"/>
            <xsl:text/>", "component": "<xsl:text/>
            <xsl:value-of select="$var_component"/>
            <xsl:text/>", "scope": "<xsl:text/>
            <xsl:value-of select="$scopeNaam"/>
            <xsl:text/>", "local": "<xsl:text/>
            <xsl:value-of select="$localName"/>
            <xsl:text/>", "melding": "De scope <xsl:text/>
            <xsl:value-of select="$scopeNaam"/>
            <xsl:text/> van de IntRef met <xsl:text/>
            <xsl:value-of select="@ref"/>
            <xsl:text/> is niet gelijk aan de naam van het doel: tekst-element <xsl:text/>
            <xsl:value-of select="$localName"/>
            <xsl:text/> met eId <xsl:text/>
            <xsl:value-of select="$doelwit_eid"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="$var_component"/>
            <xsl:text/>.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M11"/>
   <xsl:template match="@*|node()" priority="-2" mode="M11">
      <xsl:apply-templates select="*" mode="M11"/>
   </xsl:template>
   <!--PATTERN sch_tekst_028Referentie informatieobject - correcte verwijzing-->
   <!--RULE -->
   <xsl:template match="tekst:IntIoRef[not(ancestor::tekst:RegelingMutatie | ancestor::BesluitMutatie)]"
                 priority="1000"
                 mode="M13">
      <xsl:variable name="doelwit" select="@ref"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="key('alleExtIoRefVoorIntIoRefs', $doelwit)"/>
         <xsl:otherwise>
				{"code": "STOP0011", "element": "<xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/>", "ref": "<xsl:text/>
            <xsl:value-of select="$doelwit"/>
            <xsl:text/>", "melding": "De @ref van element <xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/> met waarde <xsl:text/>
            <xsl:value-of select="$doelwit"/>
            <xsl:text/> verwijst niet naar een wId van een ExtIoRef binnen hetzelfde bestand. Controleer de referentie, corrigeer of de referentie of de wId identificatie van het element waarnaar wordt verwezen", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M13"/>
   <xsl:template match="@*|node()" priority="-2" mode="M13">
      <xsl:apply-templates select="*" mode="M13"/>
   </xsl:template>
   <!--PATTERN sch_tekst_ExtIoRefExtIoRef: Referentie extern informatieobject-->
   <!--RULE -->
   <xsl:template match="tekst:ExtIoRef" priority="1000" mode="M14">
      <xsl:variable name="ref" select="normalize-space(@ref)"/>
      <xsl:variable name="reeks" select="tokenize($ref, '/')"/>
      <xsl:variable name="collectie" select="$reeks[4]"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space(.) = $ref"/>
         <xsl:otherwise>
				{"code": "STOP0012", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "De JOIN-identifier van ExtIoRef <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> in de tekst is niet gelijk aan de als referentie opgenomen JOIN-identificatie. Controleer de gebruikte JOIN-identicatie en plaats de juiste verwijzing als zowel de @ref als de tekst van het element ExtIoRef", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--REPORT fout-->
      <xsl:if test="replace($collectie, 'regdata','')">
				{"code": "STOP0092", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "ref": "<xsl:text/>
         <xsl:value-of select="$ref"/>
         <xsl:text/>", "collectie": "<xsl:text/>
         <xsl:value-of select="$collectie"/>
         <xsl:text/>", "melding": "De collectie-aanduiding '<xsl:text/>
         <xsl:value-of select="$collectie"/>
         <xsl:text/>' in de JOIN-identifier referentie <xsl:text/>
         <xsl:value-of select="$ref"/>
         <xsl:text/> in de ExtIoRef met eId <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> is niet van het juiste type. Dit mag alleen 'regdata' zijn. Voor verwijzingen naar alleen-bekend-te-maken 'pubdata' informatieobjecten moet ExtRef gebruikt worden. Corrigeer de referentie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:Inhoud"/>
         <xsl:otherwise>
				{"code": "STOP0102", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "De ExtIoRef(eId <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>) staat niet binnen een Inhoud-element. Dit is niet toegestaan. Verwijder de ExtIoRef of plaats deze binnen een Inhoud-element.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--REPORT fout-->
      <xsl:if test="ancestor::tekst:ArtikelgewijzeToelichting | ancestor::tekst:AlgemeneToelichting | ancestor::tekst:Toelichting | ancestor::tekst:Motivering">
				{"code": "STOP0103", "element": "<xsl:text/>
         <xsl:value-of select="local-name((ancestor::tekst:Toelichting | ancestor::tekst:AlgemeneToelichting | ancestor::tekst:ArtikelgewijzeToelichting | ancestor::tekst:Motivering)[last()])"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "De ExtIoRef(eId <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>) staat binnen <xsl:text/>
         <xsl:value-of select="local-name((ancestor::tekst:Toelichting | ancestor::tekst:AlgemeneToelichting | ancestor::tekst:ArtikelgewijzeToelichting | ancestor::tekst:Motivering)[last()])"/>
         <xsl:text/>. Dit is niet toegestaan. Verwijder de ExtIoRef of plaats deze in een Inhoud-element binnen het Lichaam of een (Wijzig)Bijlage van het besluit of de regeling.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M14"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M14"/>
   <xsl:template match="@*|node()" priority="-2" mode="M14">
      <xsl:apply-templates select="*" mode="M14"/>
   </xsl:template>
   <!--PATTERN sch_tekst_104Formule/Titel, Bijschrift, Bron, Lijstaanhef, Lijstsluiting - ExtIoRef niet toegestaan-->
   <!--RULE -->
   <xsl:template match="tekst:Titel[parent::tekst:Figuur]//tekst:ExtIoRef | tekst:Bijschrift//tekst:ExtIoRef | tekst:Bron//tekst:ExtIoRef | tekst:Lijstaanhef//tekst:ExtIoRef | tekst:Lijstsluiting//tekst:ExtIoRef"
                 priority="1000"
                 mode="M15">

		<!--REPORT fout-->
      <xsl:if test=".">
				{"code": "STOP0104", "element": "<xsl:text/>
         <xsl:value-of select="local-name((ancestor::tekst:Titel[parent::tekst:Figuur] | ancestor::tekst:Bijschrift | ancestor::tekst:Bron | ancestor::tekst:Lijstaanhef | ancestor::tekst:Lijstsluiting)[1])"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "De ExtIoRef(eId <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>) staat binnen <xsl:text/>
         <xsl:value-of select="local-name((ancestor::tekst:Titel[parent::tekst:Figuur] | ancestor::tekst:Bijschrift | ancestor::tekst:Bron | ancestor::tekst:Lijstaanhef | ancestor::tekst:Lijstsluiting)[1])"/>
         <xsl:text/> dit is niet toegestaan. Verwijder de ExtIoRef of verplaats deze.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M15"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M15"/>
   <xsl:template match="@*|node()" priority="-2" mode="M15">
      <xsl:apply-templates select="*" mode="M15"/>
   </xsl:template>
   <!--PATTERN sch_tekst_023RegelingTijdelijkdeel - WijzigArtikel niet toegestaan-->
   <!--RULE -->
   <xsl:template match="tekst:RegelingTijdelijkdeel//tekst:WijzigArtikel"
                 priority="1000"
                 mode="M16">

		<!--REPORT fout-->
      <xsl:if test="self::tekst:WijzigArtikel">
				{"code": "STOP0015", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het WijzigArtikel <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> is in een RegelingTijdelijkdeel niet toegestaan. Verwijder het WijzigArtikel of pas dit aan naar een Artikel indien dit mogelijk is", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M16"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M16"/>
   <xsl:template match="@*|node()" priority="-2" mode="M16">
      <xsl:apply-templates select="*" mode="M16"/>
   </xsl:template>
   <!--PATTERN sch_tekst_026RegelingCompact - WijzigArtikel niet toegestaan-->
   <!--RULE -->
   <xsl:template match="tekst:RegelingCompact//tekst:WijzigArtikel"
                 priority="1000"
                 mode="M17">

		<!--REPORT fout-->
      <xsl:if test="self::tekst:WijzigArtikel">
				{"code": "STOP0016", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het WijzigArtikel <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> is in een RegelingCompact niet toegestaan. Verwijder het WijzigArtikel of pas dit aan naar een Artikel indien dit mogelijk is", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M17"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M17"/>
   <xsl:template match="@*|node()" priority="-2" mode="M17">
      <xsl:apply-templates select="*" mode="M17"/>
   </xsl:template>
   <!--PATTERN sch_tekst_009Mutaties - Wijzigingen tekstueel-->
   <!--RULE -->
   <xsl:template match="tekst:NieuweTekst | tekst:VerwijderdeTekst"
                 priority="1000"
                 mode="M18">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:RegelingMutatie or ancestor::tekst:BesluitMutatie or ancestor::tekst:*[@vorm='proefversie']"/>
         <xsl:otherwise>
				{"code": "STOP0017", "ouder": "<xsl:text/>
            <xsl:value-of select="local-name(parent::tekst:*)"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "element": "<xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/>", "melding": "Tekstuele wijziging is niet toegestaan buiten de context van een tekst:RegelingMutatie of tekst:BesluitMutatie. element <xsl:text/>
            <xsl:value-of select="local-name(parent::tekst:*)"/>
            <xsl:text/> met id \"<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>\" bevat een <xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/>. Verwijder het element <xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/>", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M18"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M18"/>
   <xsl:template match="@*|node()" priority="-2" mode="M18">
      <xsl:apply-templates select="*" mode="M18"/>
   </xsl:template>
   <!--PATTERN sch_tekst_010Mutaties - Wijzigingen structuur-->
   <!--RULE -->
   <xsl:template match="tekst:*[@wijzigactie]" priority="1000" mode="M19">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:Vervang or ancestor::tekst:VervangKop or ancestor::tekst:*[@vorm='proefversie']"/>
         <xsl:otherwise>
				{"code": "STOP0018", "element": "<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor-or-self::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Een attribuut @wijzigactie is niet toegestaan op element <xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/> met id \"<xsl:text/>
            <xsl:value-of select="ancestor-or-self::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>\" buiten de context van Vervang. Verwijder het attribuut @wijzigactie", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M19"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M19"/>
   <xsl:template match="@*|node()" priority="-2" mode="M19">
      <xsl:apply-templates select="*" mode="M19"/>
   </xsl:template>
   <!--PATTERN sch_tekst_011Identificatie - Alle wId en eId binnen of buiten een AKN-component zijn uniek-->
   <!--RULE -->
   <xsl:template match="tekst:*[@eId][not(ancestor-or-self::tekst:WijzigInstructies)]"
                 priority="1001"
                 mode="M23">
      <xsl:variable name="mijnComponent"
                    select="./ancestor-or-self::tekst:*[@componentnaam][1]/@componentnaam"/>
      <xsl:variable name="aantalEID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="exists($mijnComponent)">
               <xsl:value-of select="count(key('alleEIDs',@eId)[ancestor-or-self::tekst:*[@componentnaam][1]/@componentnaam=$mijnComponent])"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="count(key('alleEIDs',@eId)[not(ancestor-or-self::tekst:*[@componentnaam])])"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="aantalWID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="exists($mijnComponent)">
               <xsl:value-of select="count(key('alleWIDs',@wId)[ancestor-or-self::tekst:*[@componentnaam][1]/@componentnaam=$mijnComponent])"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="count(key('alleWIDs',@wId)[not(ancestor-or-self::tekst:*[@componentnaam])])"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$aantalEID = 1"/>
         <xsl:otherwise>
				{"code": "STOP0020", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "De eId '<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>' is niet uniek. Controleer de opbouw van de eId en corrigeer deze", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$aantalWID = 1"/>
         <xsl:otherwise>
				{"code": "STOP0021", "wId": "<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>", "melding": "De wId '<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>' binnen het component is niet uniek. Controleer de opbouw van de wId en corrigeer deze", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M23"/>
   </xsl:template>
   <!--RULE -->
   <xsl:template match="tekst:Noot[not(ancestor-or-self::tekst:WijzigInstructies)]"
                 priority="1000"
                 mode="M23">
      <xsl:variable name="mijnComponent"
                    select="./ancestor-or-self::tekst:*[@componentnaam][1]/@componentnaam"/>
      <xsl:variable name="aantalNootID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="exists($mijnComponent)">
               <xsl:value-of select="count(key('alleNootIDs',@id)[ancestor-or-self::tekst:*[@componentnaam][1]/@componentnaam = $mijnComponent])"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="count(key('alleNootIDs',@id)[not(ancestor-or-self::tekst:*[@componentnaam])])"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$aantalNootID = 1"/>
         <xsl:otherwise>
				{"code": "STOP0068", "id": "<xsl:text/>
            <xsl:value-of select="@id"/>
            <xsl:text/>", "melding": "De id '<xsl:text/>
            <xsl:value-of select="@id"/>
            <xsl:text/>' is niet uniek. Controleer id en corrigeer deze.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M23"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M23"/>
   <xsl:template match="@*|node()" priority="-2" mode="M23">
      <xsl:apply-templates select="*" mode="M23"/>
   </xsl:template>
   <!--PATTERN sch_tekst_020Identificatie - AKN-naamgeving voor eId en wId-->
   <!--RULE -->
   <xsl:template match="tekst:*[@eId][not(/tekst:*[@vorm='proefversie'])]"
                 priority="1000"
                 mode="M24">
      <xsl:variable name="AKNnaam">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="matches(local-name(), 'Lichaam')">body</xsl:when>
            <xsl:when test="matches(local-name(), 'RegelingOpschrift')">longTitle</xsl:when>
            <xsl:when test="matches(local-name(), 'AlgemeneToelichting')">genrecital</xsl:when>
            <xsl:when test="matches(local-name(), '^ArtikelgewijzeToelichting$')">artrecital</xsl:when>
            <xsl:when test="matches(local-name(), 'Artikel|WijzigArtikel')">art</xsl:when>
            <xsl:when test="matches(local-name(), 'WijzigLid|Lid')">para</xsl:when>
            <xsl:when test="matches(local-name(), 'Divisietekst|Mededelingtekst|Rectificatietekst')">content</xsl:when>
            <xsl:when test="matches(local-name(), 'Divisie')">div</xsl:when>
            <xsl:when test="matches(local-name(), 'Boek')">book</xsl:when>
            <xsl:when test="matches(local-name(), 'Titel')">title</xsl:when>
            <xsl:when test="matches(local-name(), 'Deel')">part</xsl:when>
            <xsl:when test="matches(local-name(), 'Hoofdstuk')">chp</xsl:when>
            <xsl:when test="matches(local-name(), 'Afdeling')">subchp</xsl:when>
            <xsl:when test="matches(local-name(), 'Paragraaf|Subparagraaf|Subsubparagraaf')">subsec</xsl:when>
            <xsl:when test="matches(local-name(), 'WijzigBijlage|Bijlage')">cmp</xsl:when>
            <xsl:when test="matches(local-name(), 'Motivering')">acc</xsl:when>
            <xsl:when test="matches(local-name(), 'Toelichting')">recital</xsl:when>
            <xsl:when test="matches(local-name(), 'InleidendeTekst')">intro</xsl:when>
            <xsl:when test="matches(local-name(), 'Aanhef')">formula_1</xsl:when>
            <xsl:when test="matches(local-name(), 'Kadertekst')">recital</xsl:when>
            <xsl:when test="matches(local-name(), 'Sluiting')">formula_2</xsl:when>
            <xsl:when test="matches(local-name(), 'table')">table</xsl:when>
            <xsl:when test="matches(local-name(), 'Figuur')">img</xsl:when>
            <xsl:when test="matches(local-name(), 'Formule')">math</xsl:when>
            <xsl:when test="matches(local-name(), 'Citaat')">cit</xsl:when>
            <xsl:when test="matches(local-name(), 'Begrippenlijst|Lijst')">list</xsl:when>
            <xsl:when test="matches(local-name(), 'Li|Begrip')">item</xsl:when>
            <xsl:when test="matches(local-name(), 'IntIoRef|ExtIoRef')">ref</xsl:when>
            <xsl:otherwise>AKN-prefix-van-onbekend-element</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="mijnEID">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="contains(@eId, '__')">
               <xsl:value-of select="tokenize(@eId, '__')[last()]"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="@eId"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="replace($mijnEID, $AKNnaam, '')='' or starts-with(replace($mijnEID, $AKNnaam, ''),'_')"/>
         <xsl:otherwise>
				{"code": "STOP0022", "AKNdeel": "<xsl:text/>
            <xsl:value-of select="$mijnEID"/>
            <xsl:text/>", "element": "<xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/>", "waarde": "<xsl:text/>
            <xsl:value-of select="$AKNnaam"/>
            <xsl:text/>", "wId": "<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>", "melding": "De AKN-naamgeving voor eId '<xsl:text/>
            <xsl:value-of select="$mijnEID"/>
            <xsl:text/>' is niet correct voor element <xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/> met id '<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>', Dit moet zijn: '<xsl:text/>
            <xsl:value-of select="$AKNnaam"/>
            <xsl:text/>'. Pas de naamgeving voor dit element en alle onderliggende elementen aan. Controleer ook de naamgeving van de bijbehorende wId en onderliggende elementen.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="mijnNummer" select="substring-after($mijnEID, '_')"/>
      <xsl:variable name="Nummerpattern"
                    select="'^(o_[0-9]+|[A-Za-z0-9\-.]*[A-Za-z0-9\-])(_inst[0-9]+)?$'"/>
      <!--REPORT waarschuwing-->
      <xsl:if test="$mijnNummer != '' and not(matches($mijnNummer,$Nummerpattern))">
				{"code": "STOP0145", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "Nummer": "<xsl:text/>
         <xsl:value-of select="$mijnNummer"/>
         <xsl:text/>", "melding": "De volgnummer-aanduiding \"<xsl:text/>
         <xsl:value-of select="$mijnNummer"/>
         <xsl:text/>\" in het laatste deel van de @eId \"<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>\" is niet correct. Het volgnummer moet bestaan uit cijfers, letters, \"-\" en \".\" en mag niet eindigend op een \".\" of alleen een nummer voorafgegaan door \"o_\", beide eventueel gevolgd door \"_instX\" waarbij X staat voor 1 of meer cijfers", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M24"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M24"/>
   <xsl:template match="@*|node()" priority="-2" mode="M24">
      <xsl:apply-templates select="*" mode="M24"/>
   </xsl:template>
   <!--PATTERN sch_tekst_014Tabel - minimale opbouw-->
   <!--RULE -->
   <xsl:template match="tekst:table/tekst:tgroup" priority="1000" mode="M25">

		<!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="number(@cols) &gt;= 2"/>
         <xsl:otherwise>
				{"code": "STOP0029", "eId": "<xsl:text/>
            <xsl:value-of select="parent::tekst:table/@eId"/>
            <xsl:text/>", "melding": "De tabel met <xsl:text/>
            <xsl:value-of select="parent::tekst:table/@eId"/>
            <xsl:text/> heeft slechts 1 kolom, dit is niet toegestaan. Pas de tabel aan, of plaats de inhoud van de tabel naar bijvoorbeeld een element Kadertekst.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M25"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M25"/>
   <xsl:template match="@*|node()" priority="-2" mode="M25">
      <xsl:apply-templates select="*" mode="M25"/>
   </xsl:template>
   <!--PATTERN sch_tekst_093Tabel - minimaal 2 rijen-->
   <!--RULE -->
   <xsl:template match="tekst:table" priority="1000" mode="M26">
      <xsl:variable name="aantal_rijen">
         <xsl:value-of xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="count(tekst:tgroup/tekst:thead/tekst:row[not(@wijzigactie = 'verwijder')]) + count(tekst:tgroup/tekst:tbody/tekst:row[not(@wijzigactie = 'verwijder')])"/>
      </xsl:variable>
      <!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="$aantal_rijen &gt;= 2"/>
         <xsl:otherwise>
				{"code": "STOP0093", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "De tabel met <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> heeft slechts 1 rij, dit is niet toegestaan. Pas de tabel aan, of paats de inhoud van de tabel naar bijvoorbeeld het element Kadertekst.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M26"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M26"/>
   <xsl:template match="@*|node()" priority="-2" mode="M26">
      <xsl:apply-templates select="*" mode="M26"/>
   </xsl:template>
   <!--PATTERN sch_tekst_094Tabel - minimaal 3 cellen-->
   <!--RULE -->
   <xsl:template match="tekst:table" priority="1000" mode="M27">
      <xsl:variable name="aantal_cellen">
         <xsl:value-of xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="count(tekst:tgroup/tekst:thead/tekst:row[not(@wijzigactie = 'verwijder')]/tekst:entry[not(@wijzigactie = 'verwijder')]) + count(tekst:tgroup/tekst:tbody/tekst:row[not(@wijzigactie = 'verwijder')]/tekst:entry[not(@wijzigactie = 'verwijder')])"/>
      </xsl:variable>
      <!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="$aantal_cellen &gt;= 3"/>
         <xsl:otherwise>
				{"code": "STOP0094", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "De tabel met <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> heeft minder dan 3 cellen, dit is niet toegestaan. Pas de tabel aan, of paats de inhoud van de tabel naar bijvoorbeeld het element Kadertekst.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M27"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M27"/>
   <xsl:template match="@*|node()" priority="-2" mode="M27">
      <xsl:apply-templates select="*" mode="M27"/>
   </xsl:template>
   <!--PATTERN sch_tekst_016Tabel - positie en identificatie van een tabelcel-->
   <!--RULE -->
   <xsl:template match="tekst:entry[@namest and @colname]"
                 priority="1000"
                 mode="M28">
      <xsl:variable name="start" select="@namest"/>
      <xsl:variable name="col" select="@colname"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$col = $start"/>
         <xsl:otherwise>
				{"code": "STOP0033", "naam": "<xsl:text/>
            <xsl:value-of select="@namest"/>
            <xsl:text/>", "nummer": "<xsl:text/>
            <xsl:value-of select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1"/>
            <xsl:text/>", "ouder": "<xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/>", "melding": "De start van de overspanning (@namest) van de cel <xsl:text/>
            <xsl:value-of select="@namest"/>
            <xsl:text/>, in de <xsl:text/>
            <xsl:value-of select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1"/>
            <xsl:text/>e rij, van de <xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)"/>
            <xsl:text/> van tabel <xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/> is niet gelijk aan de @colname van de cel.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M28"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M28"/>
   <xsl:template match="@*|node()" priority="-2" mode="M28">
      <xsl:apply-templates select="*" mode="M28"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0032-->
   <!--RULE -->
   <xsl:template match="tekst:entry[@namest][@nameend]" priority="1000" mode="M29">
      <xsl:variable name="start" select="@namest"/>
      <xsl:variable name="end" select="@nameend"/>
      <xsl:variable name="colPosities">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="ancestor::tekst:tgroup/tekst:colspec">
            <xsl:variable name="colnum">
               <xsl:choose>
                  <xsl:when test="@colnum">
                     <xsl:value-of select="@colnum"/>
                  </xsl:when>
                  <xsl:otherwise>
                     <xsl:value-of select="position()"/>
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:variable>
            <col colnum="{$colnum}" name="{@colname}"/>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="xs:integer($colPosities/*[@name = $start]/@colnum) &lt;= xs:integer($colPosities/*[@name = $end]/@colnum)"/>
         <xsl:otherwise>
				{"code": "STOP0032", "naam": "<xsl:text/>
            <xsl:value-of select="@namest"/>
            <xsl:text/>", "nummer": "<xsl:text/>
            <xsl:value-of select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1"/>
            <xsl:text/>", "ouder": "<xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/>", "melding": "De entry met @namest \"<xsl:text/>
            <xsl:value-of select="@namest"/>
            <xsl:text/>\", van de <xsl:text/>
            <xsl:value-of select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1"/>
            <xsl:text/>e rij, van de <xsl:text/>
            <xsl:value-of select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)"/>
            <xsl:text/>, in de tabel met eId: <xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/>, heeft een positie bepaling groter dan de positie van de als @nameend genoemde cel. Corrigeer de gegevens voor de overspanning.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M29"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M29"/>
   <xsl:template match="@*|node()" priority="-2" mode="M29">
      <xsl:apply-templates select="*" mode="M29"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0036-->
   <!--RULE -->
   <xsl:template match="tekst:entry[@colname]" priority="1000" mode="M30">
      <xsl:variable name="id" select="@colname"/>
      <!--REPORT fout-->
      <xsl:if test="not(ancestor::tekst:tgroup/tekst:colspec[@colname = $id])">
				{"code": "STOP0036", "naam": "colname", "nummer": "<xsl:text/>
         <xsl:value-of select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1"/>
         <xsl:text/>", "ouder": "<xsl:text/>
         <xsl:value-of select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:table/@eId"/>
         <xsl:text/>", "melding": "De entry met @colname van de <xsl:text/>
         <xsl:value-of select="count(parent::tekst:row/preceding-sibling::tekst:row) + 1"/>
         <xsl:text/>e rij, van <xsl:text/>
         <xsl:value-of select="local-name(ancestor::tekst:thead | ancestor::tekst:tbody)"/>
         <xsl:text/>, van de tabel met id: <xsl:text/>
         <xsl:value-of select="ancestor::tekst:table/@eId"/>
         <xsl:text/> , verwijst niet naar een bestaande kolom. Controleer en corrigeer de identifier voor de kolom (@colname)", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M30"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M30"/>
   <xsl:template match="@*|node()" priority="-2" mode="M30">
      <xsl:apply-templates select="*" mode="M30"/>
   </xsl:template>
   <!--PATTERN sch_tekst_017Tabel - het aantal cellen is correct-->
   <!--RULE -->
   <xsl:template match="tekst:tgroup/tekst:thead | tekst:tgroup/tekst:tbody"
                 priority="1000"
                 mode="M31">
      <xsl:variable name="totaalCellen"
                    select="count(tekst:row[not(@wijzigactie = 'verwijder')]) * number(parent::tekst:tgroup/@cols)"/>
      <xsl:variable name="colPosities">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="parent::tekst:tgroup/tekst:colspec[not(@wijzigactie = 'verwijder')]">
            <xsl:variable name="colnum">
               <xsl:choose>
                  <xsl:when test="@colnum">
                     <xsl:value-of select="@colnum"/>
                  </xsl:when>
                  <xsl:otherwise>
                     <xsl:value-of select="position()"/>
                  </xsl:otherwise>
               </xsl:choose>
            </xsl:variable>
            <col colnum="{$colnum}" name="{@colname}"/>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="spanEinde">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="(self::tekst:tbody|self::tekst:thead)/tekst:row[not(@wijzigactie = 'verwijder')]/tekst:entry[not(@wijzigactie = 'verwijder')]">
            <xsl:variable as="xs:string?" name="namest" select="@namest"/>
            <xsl:variable as="xs:string?" name="nameend" select="@nameend"/>
            <xsl:variable as="xs:integer?"
                          name="numend"
                          select="$colPosities/*[@name = $nameend]/@colnum"/>
            <xsl:variable as="xs:integer?"
                          name="numst"
                          select="$colPosities/*[@name = $namest]/@colnum"/>
            <nr>
               <xsl:choose>
                  <xsl:when test="$numend and $numst and @morerows">
                     <xsl:value-of select="($numend - $numst + 1) * (@morerows + 1)"/>
                  </xsl:when>
                  <xsl:when test="$numend and $numst">
                     <xsl:value-of select="$numend - $numst + 1"/>
                  </xsl:when>
                  <xsl:when test="@morerows">
                     <xsl:value-of select="1 + @morerows"/>
                  </xsl:when>
                  <xsl:otherwise>1</xsl:otherwise>
               </xsl:choose>
            </nr>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="spannend" select="sum($spanEinde/*)"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="number(parent::tekst:tgroup/@cols) = count(parent::tekst:tgroup/tekst:colspec[not(@wijzigactie = 'verwijder')])"/>
         <xsl:otherwise>
				{"code": "STOP0037", "nummer": "<xsl:text/>
            <xsl:value-of select="count(parent::tekst:tgroup/tekst:colspec[not(@wijzigactie = 'verwijder')])"/>
            <xsl:text/>", "naam": "<xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/>", "aantal": "<xsl:text/>
            <xsl:value-of select="parent::tekst:tgroup/@cols"/>
            <xsl:text/>", "melding": "Het aantal colspec's (<xsl:text/>
            <xsl:value-of select="count(parent::tekst:tgroup/tekst:colspec[not(@wijzigactie = 'verwijder')])"/>
            <xsl:text/>) voor <xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/> in tabel <xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/> komt niet overeen met het aantal kolommen (<xsl:text/>
            <xsl:value-of select="parent::tekst:tgroup/@cols"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$totaalCellen = $spannend"/>
         <xsl:otherwise>
				{"code": "STOP0038", "aantal": "<xsl:text/>
            <xsl:value-of select="$spannend"/>
            <xsl:text/>", "naam": "<xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/>", "nummer": "<xsl:text/>
            <xsl:value-of select="$totaalCellen"/>
            <xsl:text/>", "melding": "Het aantal cellen in <xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/> van tabel \"<xsl:text/>
            <xsl:value-of select="ancestor::tekst:table/@eId"/>
            <xsl:text/>\" komt niet overeen met de verwachting (resultaat: <xsl:text/>
            <xsl:value-of select="$spannend"/>
            <xsl:text/> van verwachting <xsl:text/>
            <xsl:value-of select="$totaalCellen"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M31"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M31"/>
   <xsl:template match="@*|node()" priority="-2" mode="M31">
      <xsl:apply-templates select="*" mode="M31"/>
   </xsl:template>
   <!--PATTERN sch_tekst_033Externe referentie, notatie-->
   <!--RULE -->
   <xsl:template match="tekst:ExtRef" priority="1000" mode="M32">
      <xsl:variable name="notatie">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="@soort = 'AKN'">/akn/</xsl:when>
            <xsl:when test="@soort = 'JCI'">jci1</xsl:when>
            <xsl:when test="@soort = 'URL'">http</xsl:when>
            <xsl:when test="@soort = 'JOIN'">/join/</xsl:when>
            <xsl:when test="@soort = 'document'"/>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="starts-with(@ref, $notatie)"/>
         <xsl:otherwise>
				{"code": "STOP0050", "type": "<xsl:text/>
            <xsl:value-of select="@soort"/>
            <xsl:text/>", "ref": "<xsl:text/>
            <xsl:value-of select="@ref"/>
            <xsl:text/>", "melding": "De ExtRef van het type <xsl:text/>
            <xsl:value-of select="@soort"/>
            <xsl:text/> met referentie <xsl:text/>
            <xsl:value-of select="@ref"/>
            <xsl:text/> heeft niet de juiste notatie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M32"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M32"/>
   <xsl:template match="@*|node()" priority="-2" mode="M32">
      <xsl:apply-templates select="*" mode="M32"/>
   </xsl:template>
   <!--PATTERN sch_tekst_037Gereserveerd als enige element-->
   <!--RULE -->
   <xsl:template match="tekst:Gereserveerd[not(ancestor::tekst:Vervang)][not(ancestor::tekst:Artikel)]"
                 priority="1000"
                 mode="M33">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="not(following-sibling::tekst:*)"/>
         <xsl:otherwise>
				{"code": "STOP0055", "naam": "<xsl:text/>
            <xsl:value-of select="local-name(following-sibling::tekst:*[1])"/>
            <xsl:text/>", "element": "<xsl:text/>
            <xsl:value-of select="local-name(parent::tekst:*)"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="parent::tekst:*/@eId"/>
            <xsl:text/>", "melding": "Het element <xsl:text/>
            <xsl:value-of select="local-name(following-sibling::tekst:*[1])"/>
            <xsl:text/> binnen <xsl:text/>
            <xsl:value-of select="local-name(parent::tekst:*)"/>
            <xsl:text/> met eId: \"<xsl:text/>
            <xsl:value-of select="parent::tekst:*/@eId"/>
            <xsl:text/>\" is niet toegestaan na een element Gereserveerd. Verwijder het element Gereserveerd of verplaats dit element naar een eigen structuur of tekst.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M33"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M33"/>
   <xsl:template match="@*|node()" priority="-2" mode="M33">
      <xsl:apply-templates select="*" mode="M33"/>
   </xsl:template>
   <!--PATTERN sch_tekst_069Eén type element in Lid, tenzij binnen vervang-->
   <!--RULE -->
   <xsl:template match="tekst:Lid[not(ancestor::tekst:Vervang)]"
                 priority="1000"
                 mode="M34">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(child::tekst:*[not(self::tekst:LidNummer)])=1"/>
         <xsl:otherwise>
				{"code": "STOP0069", "naam": "<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "Het <xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/> met eId '<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>' heeft een combinatie van elementen dat niet is toegestaan. Slechts één type element is toegestaan. Corrigeer dit door de combinatie van verschillende type elementen te verwijderen.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M34"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M34"/>
   <xsl:template match="@*|node()" priority="-2" mode="M34">
      <xsl:apply-templates select="*" mode="M34"/>
   </xsl:template>
   <!--PATTERN sch_tekst_070Eén type element in Artikel, tenzij binnen vervang (of oude plek van een verplaatst artikel in een proefversie)-->
   <!--RULE -->
   <xsl:template match="tekst:Artikel[not(ancestor::tekst:Vervang)][not(@wijzigactie='verplaatstNaar')]"
                 priority="1000"
                 mode="M35">
      <xsl:variable name="aantalKinderenNietLid"
                    select="count(tekst:Inhoud|tekst:Vervallen|tekst:Gereserveerd|tekst:NogNietInWerking)"/>
      <!--REPORT fout-->
      <xsl:if test="(count(child::tekst:*[not(self::tekst:Kop)])=0) or (child::tekst:Lid and $aantalKinderenNietLid&gt;0) or ($aantalKinderenNietLid&gt;1)">
				{"code": "STOP0070", "naam": "<xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het <xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/> met eId '<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>' heeft een combinatie van elementen dat niet is toegestaan. Slechts één type element is toegestaan. Corrigeer dit door de combinatie van verschillende type elementen te verwijderen.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M35"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M35"/>
   <xsl:template match="@*|node()" priority="-2" mode="M35">
      <xsl:apply-templates select="*" mode="M35"/>
   </xsl:template>
   <!--PATTERN sch_tekst_039Structuur compleet-->
   <!--RULE -->
   <xsl:template match="tekst:Afdeling | tekst:Bijlage | tekst:Boek | tekst:Deel | tekst:Divisie | tekst:Hoofdstuk | tekst:Paragraaf | tekst:Subparagraaf | tekst:Subsubparagraaf | tekst:Titel[not(parent::tekst:Figuur)]"
                 priority="1000"
                 mode="M36">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="child::tekst:*[not(self::tekst:Kop)] or ancestor::tekst:Vervang or ancestor::tekst:VoegToe or ancestor::tekst:Verwijder or @wijzigactie='verplaatstNaar'"/>
         <xsl:otherwise>
				{"code": "STOP0058", "naam": "<xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "Het element <xsl:text/>
            <xsl:value-of select="name(.)"/>
            <xsl:text/> met eId: \"<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> is niet compleet, een kind-element anders dan een Kop is verplicht. Completeer of verwijder dit structuur-element.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M36"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M36"/>
   <xsl:template match="@*|node()" priority="-2" mode="M36">
      <xsl:apply-templates select="*" mode="M36"/>
   </xsl:template>
   <!--PATTERN sch_tekst_041Divisietekst compleet-->
   <!--RULE -->
   <xsl:template match="tekst:Divisietekst[not(ancestor::tekst:Vervang)]"
                 priority="1000"
                 mode="M37">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(child::tekst:*[not(self::tekst:Kop)])=1"/>
         <xsl:otherwise>
				{"code": "STOP0060", "naam": "<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="xs:string(@eId)"/>
            <xsl:text/>", "melding": "Het element <xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/> met eId: \"<xsl:text/>
            <xsl:value-of select="xs:string(@eId)"/>
            <xsl:text/> is niet correct, één kind-element naast Kop is verplicht. Completeer of verwijder dit element.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M37"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M37"/>
   <xsl:template match="@*|node()" priority="-2" mode="M37">
      <xsl:apply-templates select="*" mode="M37"/>
   </xsl:template>
   <!--PATTERN sch_tekst_044Vervallen structuur-->
   <!--RULE -->
   <xsl:template match="tekst:Vervallen[not(ancestor::tekst:Vervang)][not(parent::tekst:Artikel)][not(parent::tekst:Lid)][not(parent::tekst:Divisietekst)]"
                 priority="1000"
                 mode="M38">

		<!--REPORT fout-->
      <xsl:if test="following-sibling::tekst:*[not(child::tekst:Vervallen)]">
				{"code": "STOP0062", "naam": "<xsl:text/>
         <xsl:value-of select="local-name(parent::tekst:*)"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="parent::tekst:*/@eId"/>
         <xsl:text/>", "element": "<xsl:text/>
         <xsl:value-of select="local-name(following-sibling::tekst:*[not(child::tekst:Vervallen)][1])"/>
         <xsl:text/>", "id": "<xsl:text/>
         <xsl:value-of select="following-sibling::tekst:*[not(child::tekst:Vervallen)][1]/@eId"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="local-name(parent::tekst:*)"/>
         <xsl:text/> met eId: \"<xsl:text/>
         <xsl:value-of select="parent::tekst:*/@eId"/>
         <xsl:text/>\" is vervallen, maar heeft minstens nog een niet vervallen element\". Controleer vanaf element <xsl:text/>
         <xsl:value-of select="local-name(following-sibling::tekst:*[not(child::tekst:Vervallen)][1])"/>
         <xsl:text/> met eId \"<xsl:text/>
         <xsl:value-of select="following-sibling::tekst:*[not(child::tekst:Vervallen)][1]/@eId"/>
         <xsl:text/> of alle onderliggende elementen als vervallen zijn aangemerkt.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M38"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M38"/>
   <xsl:template match="@*|node()" priority="-2" mode="M38">
      <xsl:apply-templates select="*" mode="M38"/>
   </xsl:template>
   <!--PATTERN sch_tekst_STOP0087NogNietInWerking structuur-->
   <!--RULE -->
   <xsl:template match="tekst:NogNietInWerking[not(ancestor::tekst:Vervang)][not(parent::tekst:Artikel)][not(parent::tekst:Lid)][not(parent::tekst:Divisietekst)]"
                 priority="1000"
                 mode="M39">

		<!--REPORT fout-->
      <xsl:if test="following-sibling::tekst:*[not(child::tekst:NogNietInWerking)]">
				{"code": "STOP0087", "naam": "<xsl:text/>
         <xsl:value-of select="local-name(parent::tekst:*)"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="parent::tekst:*/@eId"/>
         <xsl:text/>", "element": "<xsl:text/>
         <xsl:value-of select="local-name(following-sibling::tekst:*[not(child::tekst:NogNietInWerking)][1])"/>
         <xsl:text/>", "id": "<xsl:text/>
         <xsl:value-of select="following-sibling::tekst:*[not(child::tekst:NogNietInWerking)][1]/@eId"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="local-name(parent::tekst:*)"/>
         <xsl:text/> met eId: \"<xsl:text/>
         <xsl:value-of select="parent::tekst:*/@eId"/>
         <xsl:text/>\" is 'Nog niet in werking', maar heeft minstens nog één child-element dat niet 'Nog niet in werking' is. Controleer vanaf element <xsl:text/>
         <xsl:value-of select="local-name(following-sibling::tekst:*[not(child::tekst:NogNietInWerking)][1])"/>
         <xsl:text/> met eId \"<xsl:text/>
         <xsl:value-of select="following-sibling::tekst:*[not(child::tekst:NogNietInWerking)][1]/@eId"/>
         <xsl:text/> of alle onderliggende elementen als 'Nog niet in werking' zijn aangemerkt.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M39"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M39"/>
   <xsl:template match="@*|node()" priority="-2" mode="M39">
      <xsl:apply-templates select="*" mode="M39"/>
   </xsl:template>
   <!--PATTERN sch_tekst_045-->
   <!--RULE -->
   <xsl:template match="tekst:Contact" priority="1000" mode="M40">
      <xsl:variable name="pattern">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="@soort = 'e-mail'">[^@]+@[^\.]+\..+</xsl:when>
            <xsl:otherwise>[onbekend-soort-adres]</xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="adres" select="@adres/./string()"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches($adres, $pattern)"/>
         <xsl:otherwise>
				{"code": "STOP0064", "adres": "<xsl:text/>
            <xsl:value-of select="./string()"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het e-mailadres <xsl:text/>
            <xsl:value-of select="./string()"/>
            <xsl:text/> zoals genoemd in het element Contact met eId <xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/> moet een correct geformatteerd e-mailadres zijn. Corrigeer het e-mailadres.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M40"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M40"/>
   <xsl:template match="@*|node()" priority="-2" mode="M40">
      <xsl:apply-templates select="*" mode="M40"/>
   </xsl:template>
   <!--PATTERN sch_tekst_046-->
   <!--RULE -->
   <xsl:template match="tekst:Motivering[@schemaversie]" priority="1000" mode="M41">

		<!--REPORT fout-->
      <xsl:if test="ancestor::tekst:BesluitCompact|ancestor::tekst:BesluitKlassiek">
				{"code": "STOP0075", "schemaversie": "<xsl:text/>
         <xsl:value-of select="@schemaversie"/>
         <xsl:text/>", "melding": "Het attribuut schemaversie (met waarde <xsl:text/>
         <xsl:value-of select="@schemaversie"/>
         <xsl:text/>) bij tekst:Motivering mag niet gebruikt worden binnen tekst:BesluitCompact of tekst:BesluitKlassiek. Verwijder het attribuut schemaversie bij tekst:Motivering", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M41"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M41"/>
   <xsl:template match="@*|node()" priority="-2" mode="M41">
      <xsl:apply-templates select="*" mode="M41"/>
   </xsl:template>
   <!--PATTERN sch_tekst_081Toelichting specifiek-->
   <!--RULE -->
   <xsl:template match="tekst:Toelichting[not(parent::tekst:BesluitCompact | parent::tekst:BesluitKlassiek)]"
                 priority="1000"
                 mode="M42">

		<!--REPORT ontraden-->
      <xsl:if test="child::tekst:Divisie | child::tekst:Divisietekst">
      			{"code": "STOP0081", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "De Regeling heeft een Toelichting met eId <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> met een structuur met Divisie of Divisietekst. Dat zal in de toekomst niet meer toegestaan zijn. Advies is om deze Divisie / Divisietekst elementen in een element AlgemeneToelichting of ArtikelgewijzeToelichting te plaatsen.", "ernst": "ontraden"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M42"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M42"/>
   <xsl:template match="@*|node()" priority="-2" mode="M42">
      <xsl:apply-templates select="*" mode="M42"/>
   </xsl:template>
   <!--PATTERN -->
   <!--RULE -->
   <xsl:template match="tekst:Toelichting" priority="1000" mode="M43">
      <xsl:variable name="aantalKinderen"
                    select="count(tekst:ArtikelgewijzeToelichting[not(@wijzigactie='verwijder')] |                                             tekst:AlgemeneToelichting[not(@wijzigactie='verwijder')])"/>
      <!--REPORT fout-->
      <xsl:if test="xs:int($aantalKinderen) &gt;1 and (not(child::tekst:Kop) or child::tekst:Kop[@wijzigactie='verwijder'])">
      			{"code": "STOP0084", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het element Toelichting met eId <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> moet een Kop hebben omdat zowel een ArtikelgewijzeToelichting en een AlgemeneToelichting in de Toelichting zijn opgenomen. Geef de Toelichting een Kop met duidelijke tekstuele omschrijving.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="xs:int($aantalKinderen) = 1 and child::tekst:Kop[not(@wijzigactie='verwijder')]">
      			{"code": "STOP0085", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "localName": "<xsl:text/>
         <xsl:value-of select="local-name(child::tekst:*[2])"/>
         <xsl:text/>", "melding": "Het element Toelichting met eId <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> heeft een Kop; deze is niet toegestaan omdat het enige onderliggende element <xsl:text/>
         <xsl:value-of select="local-name(child::tekst:*[2])"/>
         <xsl:text/> al een Kop heeft. Verwijder de Kop voor het element Toelichting.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M43"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M43"/>
   <xsl:template match="@*|node()" priority="-2" mode="M43">
      <xsl:apply-templates select="*" mode="M43"/>
   </xsl:template>
   <!--PATTERN sch_tekst_082ArtikelgewijzeToelichting buiten Toelichting-->
   <!--RULE -->
   <xsl:template match="tekst:ArtikelgewijzeToelichting[not(ancestor::tekst:Verwijder | ancestor::tekst:Vervang | ancestor::tekst:VoegToe)]"
                 priority="1000"
                 mode="M44">

		<!--ASSERT ontraden-->
      <xsl:choose>
         <xsl:when test="parent::tekst:Toelichting"/>
         <xsl:otherwise>
      {"code": "STOP0082", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "De Toelichting met eId <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> heeft een structuur met Divisie of Divisietekst dat zal in de toekomst niet meer toegestaan zijn. Advies is om deze Divisie / Divisietekst elementen in een element AlgemeneToelichting of ArtikelgewijzeToelichting te plaatsen indien mogelijk.", "ernst": "ontraden"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M44"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M44"/>
   <xsl:template match="@*|node()" priority="-2" mode="M44">
      <xsl:apply-templates select="*" mode="M44"/>
   </xsl:template>
   <!--PATTERN sch_tekst_096Ontraden toelichting binnen RegelingKlassiek-->
   <!--RULE -->
   <xsl:template match="tekst:Toelichting[parent::tekst:RegelingKlassiek] | tekst:ArtikelgewijzeToelichting[parent::tekst:RegelingKlassiek]"
                 priority="1000"
                 mode="M45">

		<!--REPORT ontraden-->
      <xsl:if test=".">
      			{"code": "STOP0096", "element": "<xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>", "wId": "<xsl:text/>
         <xsl:value-of select="@wId"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/> met wId <xsl:text/>
         <xsl:value-of select="@wId"/>
         <xsl:text/> wordt ontraden in RegelingKlassiek. Rijksregelgeving kent normaliter geen te consolideren toelichtingen. Gebruik Toelichting in BesluitKlassiek voor toelichting op Rijksregelgeving.", "ernst": "ontraden"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M45"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M45"/>
   <xsl:template match="@*|node()" priority="-2" mode="M45">
      <xsl:apply-templates select="*" mode="M45"/>
   </xsl:template>
   <!--PATTERN sch_tekst_089Vaste @eId's en @wId's zonder toevoeging-->
   <!--RULE -->
   <xsl:template match="tekst:Lichaam | tekst:RegelingOpschrift | tekst:Aanhef | tekst:Sluiting | tekst:Toelichting | tekst:ArtikelgewijzeToelichting | tekst:AlgemeneToelichting | tekst:Motivering | tekst:Inhoudsopgave"
                 priority="1000"
                 mode="M46">
      <xsl:variable name="patroon"
                    select="'^(body|formula_1|formula_2|longTitle|recital|genrecital|artrecital|acc|toc)$'"/>
      <xsl:variable name="vpatroon"
                    select="'^(formula_1|formula_2|longTitle|recital|genrecital|artrecital|acc|toc)_inst[0-9]+$'"/>
      <xsl:variable name="mijnNaam">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="self::tekst:Lichaam">body</xsl:when>
            <xsl:when test="self::tekst:RegelingOpschrift">longTitle</xsl:when>
            <xsl:when test="self::tekst:Aanhef">formula_1</xsl:when>
            <xsl:when test="self::tekst:Sluiting">formula_2</xsl:when>
            <xsl:when test="self::tekst:Toelichting">recital</xsl:when>
            <xsl:when test="self::tekst:ArtikelgewijzeToelichting">artrecital</xsl:when>
            <xsl:when test="self::tekst:AlgemeneToelichting">genrecital</xsl:when>
            <xsl:when test="self::tekst:Motivering">acc</xsl:when>
            <xsl:when test="self::tekst:Inhoudsopgave">toc</xsl:when>
         </xsl:choose>
      </xsl:variable>
      <xsl:variable name="wIdtoevoeging">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="self::tekst:Sluiting">
               <xsl:value-of select="replace(substring-after(@wId, 'formula_2'), '^_inst[0-9]+', '')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="substring-after(@wId, $mijnNaam)"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(@wId, $patroon) or          ((ancestor::tekst:Verwijder or ancestor::tekst:*[@wijzigactie='verwijder'] or self::tekst:Sluiting) and matches(@wId,$vpatroon))"/>
         <xsl:otherwise>
				{"code": "STOP0089", "wId": "<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>", "element": "<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>", "toevoeging": "<xsl:text/>
            <xsl:value-of select="$wIdtoevoeging"/>
            <xsl:text/>", "voorvoeging": "<xsl:text/>
            <xsl:value-of select="substring-before(@wId, $mijnNaam)"/>
            <xsl:text/>", "melding": "Vaste identificatie elementen hebben als 'wId' alleen de vaste identificatie. 'wId' <xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/> van het element <xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/> heeft een voorvoeging '<xsl:text/>
            <xsl:value-of select="substring-before(@wId, $mijnNaam)"/>
            <xsl:text/>' en/of een toevoeging '<xsl:text/>
            <xsl:value-of select="$wIdtoevoeging"/>
            <xsl:text/>'. Dit is niet toegestaan. Verwijder de voor- of toevoeging van de wId.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="eIdtoevoeging">
         <xsl:choose xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                     xmlns:sqf="http://www.schematron-quickfix.com/validator/process">
            <xsl:when test="self::tekst:Sluiting">
               <xsl:value-of select="replace(substring-after(@eId, 'formula_2'), '^_inst[0-9]+', '')"/>
            </xsl:when>
            <xsl:otherwise>
               <xsl:value-of select="substring-after(@eId, $mijnNaam)"/>
            </xsl:otherwise>
         </xsl:choose>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="matches(@eId, $patroon) or          ((ancestor::tekst:Verwijder or ancestor::tekst:*[@wijzigactie='verwijder'] or self::tekst:Sluiting) and matches(@eId,$vpatroon))"/>
         <xsl:otherwise>
				{"code": "STOP0090", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "element": "<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>", "toevoeging": "<xsl:text/>
            <xsl:value-of select="$eIdtoevoeging"/>
            <xsl:text/>", "melding": "Het 'eId' <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> van het element <xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/> heeft een toevoeging <xsl:text/>
            <xsl:value-of select="$eIdtoevoeging"/>
            <xsl:text/>. Dit is niet toegestaan. Alleen om een Sluiting uniek te maken of binnen een mutatie met een verwijdering van het element, is een '_instX' toevoeging toegestaan. Verwijder de toevoeging '<xsl:text/>
            <xsl:value-of select="$eIdtoevoeging"/>
            <xsl:text/>' van de eId.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M46"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M46"/>
   <xsl:template match="@*|node()" priority="-2" mode="M46">
      <xsl:apply-templates select="*" mode="M46"/>
   </xsl:template>
   <!--PATTERN sch_tekst_091@eId begint met @eId voorouder-->
   <!--RULE -->
   <xsl:template match="tekst:*[@eId][not(parent::tekst:Vervang or parent::tekst:Verwijder or parent::tekst:VoegToe or parent::tekst:*[@wijzigactie='verwijderContainer'] or ancestor::tekst:WijzigInstructies)]"
                 priority="1000"
                 mode="M47">
      <xsl:variable name="ancestorID" select="ancestor::tekst:*[@eId][1]/@eId"/>
      <xsl:variable name="rest" select="substring-after(@eId, $ancestorID)"/>
      <!--REPORT fout-->
      <xsl:if test="contains(@eId, '__') and (not(starts-with($rest, '__')) or not(starts-with(@eId, $ancestorID)))">
				{"code": "STOP0091", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "element": "<xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>", "topId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "topElement": "<xsl:text/>
         <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "melding": "De eId <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> van <xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/> is niet correct. Deze moet beginnen met <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/> van het bovenliggende element <xsl:text/>
         <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M47"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M47"/>
   <xsl:template match="@*|node()" priority="-2" mode="M47">
      <xsl:apply-templates select="*" mode="M47"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0097strong en u ontraden in koppen-->
   <!--RULE -->
   <xsl:template match="tekst:u[ancestor::tekst:Opschrift | ancestor::tekst:Subtitel |  ancestor::tekst:Tussenkop | ancestor::tekst:title | ancestor::tekst:Titel[parent::tekst:Figuur]] |     tekst:strong[ancestor::tekst:Opschrift | ancestor::tekst:Subtitel | ancestor::tekst:Tussenkop | ancestor::tekst:title | ancestor::tekst:Titel[parent::tekst:Figuur]]"
                 priority="1000"
                 mode="M48">

		<!--REPORT waarschuwing-->
      <xsl:if test=".">
				{"code": "STOP0097", "element": "<xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>", "parent": "<xsl:text/>
         <xsl:value-of select="local-name(..)"/>
         <xsl:text/>", "top-eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "topElement": "<xsl:text/>
         <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/> binnen <xsl:text/>
         <xsl:value-of select="local-name(..)"/>
         <xsl:text/> van het bovenliggende element <xsl:text/>
         <xsl:value-of select="local-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/> met eId=\"<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>\" is niet toegestaan. De opmaak kan conflicteren met Kopopmaak. Verwijder het element <xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M48"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M48"/>
   <xsl:template match="@*|node()" priority="-2" mode="M48">
      <xsl:apply-templates select="*" mode="M48"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0101RegelingKlassiek - attribuut categorieKlassiek toegestaan-->
   <!--RULE -->
   <xsl:template match="tekst:Artikel[@categorieKlassiek]"
                 priority="1000"
                 mode="M49">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:RegelingKlassiek"/>
         <xsl:otherwise>
				{"code": "STOP0101", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "Het Artikel met eId <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> heeft attribuut @categorieKlassiek. Dit is alleen toegestaan in een RegelingKlassiek. Verwijder het attribuut @categorieKlassiek.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M49"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M49"/>
   <xsl:template match="@*|node()" priority="-2" mode="M49">
      <xsl:apply-templates select="*" mode="M49"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0105Formule, Figuur niet binnen Noot-->
   <!--RULE -->
   <xsl:template match="tekst:Formule[ancestor::tekst:Noot] | tekst:Figuur[ancestor::tekst:Noot]"
                 priority="1000"
                 mode="M50">

		<!--REPORT ontraden-->
      <xsl:if test=".">
				{"code": "STOP0105", "element": "<xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/> met <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> staat binnen Noot. Dit wordt afgeraden. Verplaats <xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/> indien mogelijk.", "ernst": "ontraden"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M50"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M50"/>
   <xsl:template match="@*|node()" priority="-2" mode="M50">
      <xsl:apply-templates select="*" mode="M50"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0106Formule, Figuur, table niet Aanhef-->
   <!--RULE -->
   <xsl:template match="tekst:Formule[ancestor::tekst:Aanhef] | tekst:Figuur[ancestor::tekst:Aanhef] | tekst:table[ancestor::tekst:Aanhef]"
                 priority="1000"
                 mode="M51">

		<!--REPORT fout-->
      <xsl:if test=".">
				{"code": "STOP0106", "element": "<xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/> met <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> staat binnen Aanhef. Dit is niet toegestaan. Verwijder de <xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/> of verplaats deze.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M51"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M51"/>
   <xsl:template match="@*|node()" priority="-2" mode="M51">
      <xsl:apply-templates select="*" mode="M51"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0107Formule, Figuur, table niet Rectificatietekst-->
   <!--RULE -->
   <xsl:template match="tekst:Formule[ancestor::tekst:Rectificatietekst] | tekst:Figuur[ancestor::tekst:Rectificatietekst] | tekst:table[ancestor::tekst:Rectificatietekst]"
                 priority="1000"
                 mode="M52">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::tekst:RegelingMutatie or ancestor::tekst:BesluitMutatie"/>
         <xsl:otherwise>
				{"code": "STOP0107", "element": "<xsl:text/>
            <xsl:value-of select="local-name(.)"/>
            <xsl:text/>", "eId": "<xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/>", "melding": "Het element <xsl:text/>
            <xsl:value-of select="local-name(.)"/>
            <xsl:text/> met <xsl:text/>
            <xsl:value-of select="@eId"/>
            <xsl:text/> staat binnen Rectificatietekst. Dit is niet toegestaan. Verwijder de <xsl:text/>
            <xsl:value-of select="local-name(.)"/>
            <xsl:text/> of verplaats deze.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M52"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M52"/>
   <xsl:template match="@*|node()" priority="-2" mode="M52">
      <xsl:apply-templates select="*" mode="M52"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0108Formule, Figuur, table niet Definitie-->
   <!--RULE -->
   <xsl:template match="tekst:Formule[ancestor::tekst:Definitie] | tekst:Figuur[ancestor::tekst:Definitie] | tekst:table[ancestor::tekst:Definitie]"
                 priority="1000"
                 mode="M53">

		<!--REPORT fout-->
      <xsl:if test=".">
				{"code": "STOP0108", "element": "<xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/>", "eId": "<xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/> met <xsl:text/>
         <xsl:value-of select="@eId"/>
         <xsl:text/> staat binnen Definitie. Dit is niet toegestaan. Verwijder de <xsl:text/>
         <xsl:value-of select="local-name(.)"/>
         <xsl:text/> of verplaats deze.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M53"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M53"/>
   <xsl:template match="@*|node()" priority="-2" mode="M53">
      <xsl:apply-templates select="*" mode="M53"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0109i niet recursief-->
   <!--RULE -->
   <xsl:template match="tekst:i[ancestor::tekst:i[not(descendant::tekst:Noot)]]"
                 priority="1000"
                 mode="M54">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor-or-self::tekst:*[@wijzigactie = 'verwijder'] | ancestor::tekst:Verwijder | ancestor::tekst:VerwijderdeTekst"/>
         <xsl:otherwise>
				{"code": "STOP0109", "parent": "<xsl:text/>
            <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/>", "parent-eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het element i in <xsl:text/>
            <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/> met <xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/> staat binnen een ander element i. Dit is niet toegestaan. Verwijder of vervang een van de twee elementen door een ander nadruk-element.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M54"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M54"/>
   <xsl:template match="@*|node()" priority="-2" mode="M54">
      <xsl:apply-templates select="*" mode="M54"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0110u niet recursief-->
   <!--RULE -->
   <xsl:template match="tekst:u[ancestor::tekst:u[not(descendant::tekst:Noot)]]"
                 priority="1000"
                 mode="M55">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor-or-self::tekst:*[@wijzigactie = 'verwijder'] | ancestor::tekst:Verwijder | ancestor::tekst:VerwijderdeTekst"/>
         <xsl:otherwise>
				{"code": "STOP0110", "parent": "<xsl:text/>
            <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/>", "parent-eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het element u in <xsl:text/>
            <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/> met <xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/> staat binnen een ander element u. Dit is niet toegestaan. Verwijder of vervang een van de twee elementen door een ander nadruk-element.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M55"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M55"/>
   <xsl:template match="@*|node()" priority="-2" mode="M55">
      <xsl:apply-templates select="*" mode="M55"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0111strong niet recursief-->
   <!--RULE -->
   <xsl:template match="tekst:strong[ancestor::tekst:strong[not(descendant::tekst:Noot)]]"
                 priority="1000"
                 mode="M56">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor-or-self::tekst:*[@wijzigactie = 'verwijder'] | ancestor::tekst:Verwijder | ancestor::tekst:VerwijderdeTekst"/>
         <xsl:otherwise>
				{"code": "STOP0111", "parent": "<xsl:text/>
            <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/>", "parent-eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het element strong in <xsl:text/>
            <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/> met <xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/> staat binnen een ander element strong. Dit is niet toegestaan. Verwijder of vervang een van de twee elementen door een ander nadruk-element.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M56"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M56"/>
   <xsl:template match="@*|node()" priority="-2" mode="M56">
      <xsl:apply-templates select="*" mode="M56"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0112b niet recursief-->
   <!--RULE -->
   <xsl:template match="tekst:b[ancestor::tekst:b[not(descendant::tekst:Noot)]]"
                 priority="1000"
                 mode="M57">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor-or-self::tekst:*[@wijzigactie = 'verwijder'] | ancestor::tekst:Verwijder | ancestor::tekst:VerwijderdeTekst"/>
         <xsl:otherwise>
				{"code": "STOP0112", "parent": "<xsl:text/>
            <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/>", "parent-eId": "<xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/>", "melding": "Het element b in <xsl:text/>
            <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
            <xsl:text/> met <xsl:text/>
            <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
            <xsl:text/> staat binnen een ander element b. Dit is niet toegestaan. Verwijder of vervang een van de twee elementen door een ander nadruk-element.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M57"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M57"/>
   <xsl:template match="@*|node()" priority="-2" mode="M57">
      <xsl:apply-templates select="*" mode="M57"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0113link niet in een andere link-->
   <!--RULE -->
   <xsl:template match="tekst:ExtRef | tekst:ExtIoRef | tekst:IntIoRef | tekst:IntRef |tekst:Contact"
                 priority="1000"
                 mode="M58">

		<!--REPORT fout-->
      <xsl:if test="ancestor::tekst:IntIoRef or ancestor::tekst:IntRef or ancestor::tekst:ExtRef">
				{"code": "STOP0113", "element": "<xsl:text/>
         <xsl:value-of select="node-name(.)"/>
         <xsl:text/>", "parent": "<xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "parent-eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "Het element <xsl:text/>
         <xsl:value-of select="node-name(.)"/>
         <xsl:text/> in <xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/> met <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/> staat binnen een ander link-element. Dit is niet toegestaan. Verwijder de link uit de link.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M58"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M58"/>
   <xsl:template match="@*|node()" priority="-2" mode="M58">
      <xsl:apply-templates select="*" mode="M58"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0114noot niet recursief-->
   <!--RULE -->
   <xsl:template match="tekst:Noot" priority="1000" mode="M59">

		<!--REPORT fout-->
      <xsl:if test="ancestor::tekst:Noot">
				{"code": "STOP0114", "parent": "<xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "parent-eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "Het element noot in <xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/> met <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/> staat binnen een ander element noot. Dit is niet toegestaan. Verwijder de noot binnen de noot.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M59"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M59"/>
   <xsl:template match="@*|node()" priority="-2" mode="M59">
      <xsl:apply-templates select="*" mode="M59"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0115InlineTekstAfbeelding bij voorkeur niet gebruiken-->
   <!--RULE -->
   <xsl:template match="tekst:InlineTekstAfbeelding" priority="1000" mode="M60">

		<!--REPORT waarschuwing-->
      <xsl:if test=".">
				{"code": "STOP0115", "parent": "<xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "parent-eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "Het element InlineTekstAfbeelding komt voor in <xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/> met <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>. Het gebruik van dit element wordt afgeraden. Gebruik indien mogelijk een UTF-8 karakter om betreffend teken weer te geven.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M60"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M60"/>
   <xsl:template match="@*|node()" priority="-2" mode="M60">
      <xsl:apply-templates select="*" mode="M60"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0116Redactioneel bij voorkeur niet gebruiken-->
   <!--RULE -->
   <xsl:template match="tekst:Redactioneel" priority="1000" mode="M61">

		<!--REPORT waarschuwing-->
      <xsl:if test=".">
				{"code": "STOP0116", "parent": "<xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "parent-eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "Het element Redactioneel komt voor in <xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/> met <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>. Het gebruik van dit element wordt afgeraden.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M61"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M61"/>
   <xsl:template match="@*|node()" priority="-2" mode="M61">
      <xsl:apply-templates select="*" mode="M61"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0140InleidendeTekst bij voorkeur niet gebruiken-->
   <!--RULE -->
   <xsl:template match="tekst:InleidendeTekst" priority="1000" mode="M62">

		<!--REPORT ontraden-->
      <xsl:if test=".">
				{"code": "STOP0140", "parent": "<xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/>", "parent-eId": "<xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>", "melding": "Het element InleidendeTekst komt voor in <xsl:text/>
         <xsl:value-of select="node-name(ancestor::tekst:*[@eId][1])"/>
         <xsl:text/> met <xsl:text/>
         <xsl:value-of select="ancestor::tekst:*[@eId][1]/@eId"/>
         <xsl:text/>. Het gebruik van dit element wordt afgeraden.", "ernst": "ontraden"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M62"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M62"/>
   <xsl:template match="@*|node()" priority="-2" mode="M62">
      <xsl:apply-templates select="*" mode="M62"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0142RegelingOpschrift Klassiek: bij voorkeur in BesluitKlassiek-->
   <!--RULE -->
   <xsl:template match="tekst:BesluitKlassiek" priority="1000" mode="M63">

		<!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="child::tekst:RegelingOpschrift"/>
         <xsl:otherwise>
				{"code": "STOP0142", "wordt": "<xsl:text/>
            <xsl:value-of select="./tekst:RegelingKlassiek/@wordt"/>
            <xsl:text/>", "melding": "Het BesluitKlassiek dat RegelingKlassiek \"<xsl:text/>
            <xsl:value-of select="./tekst:RegelingKlassiek/@wordt"/>
            <xsl:text/>\" instelt heeft geen RegelingOpschrift. Plaats het Opschrift van de Regeling bij voorkeur in BesluitKlassiek/RegelingOpschrift in plaats van in het RegelingKlassiek/RegelingOpschrift.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M63"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M63"/>
   <xsl:template match="@*|node()" priority="-2" mode="M63">
      <xsl:apply-templates select="*" mode="M63"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0143RegelingOpschrift Klassiek aanwezig-->
   <!--RULE -->
   <xsl:template match="tekst:BesluitKlassiek" priority="1000" mode="M64">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="descendant::tekst:RegelingOpschrift"/>
         <xsl:otherwise>
				{"code": "STOP0143", "wordt": "<xsl:text/>
            <xsl:value-of select="./tekst:RegelingKlassiek/@wordt"/>
            <xsl:text/>", "melding": "Het RegelingOpschrift voor het BesluitKlassiek dat RegelingKlassiek \"<xsl:text/>
            <xsl:value-of select="./tekst:RegelingKlassiek/@wordt"/>
            <xsl:text/>\" instelt ontbreekt. Voeg het RegelingOpschrift toe, bij voorkeur in BesluitKlassiek/RegelingOpschrift.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M64"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M64"/>
   <xsl:template match="@*|node()" priority="-2" mode="M64">
      <xsl:apply-templates select="*" mode="M64"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0146wId correct: STOP0146 BGcode, STOP0147 versienummer, STOP0148 laatste deel @wId voldoet aan eId formaat-->
   <!--RULE -->
   <xsl:template match="tekst:*[not(self::tekst:Lichaam | self::tekst:RegelingOpschrift | self::tekst:Aanhef | self::tekst:Sluiting | self::tekst:Toelichting | self::tekst:ArtikelgewijzeToelichting | self::tekst:AlgemeneToelichting | self::tekst:Motivering | self::tekst:Inhoudsopgave)][@wId]"
                 priority="1000"
                 mode="M65">
      <xsl:variable name="BGpattern"
                    select="'^(mnre[0-9]{4}|mn[0-9]{3}|gm[0-9]{4}|ws[0-9]{4}|pv[0-9]{2})$'"/>
      <xsl:variable name="VersienummerPattern" select="'^[A-Za-z0-9\-]{1,32}$'"/>
      <xsl:variable name="eIdDeelPattern"
                    select="'^(__(formula_1|formula_2|longTitle|acc|artrecital|genrecital|recital|((subchp|art|item|intro|list|cmp|book|cit|part|div|content|part|ref|img|math|chp|recital|para|subsec|table|title)_(o_[0-9]+|[A-Za-z0-9\-.]*[A-Za-z0-9\-])))(_inst[0-9]+)?)+(_moved)?$'"/>
      <xsl:variable name="mijnBGcode" select="tokenize(@wId,'_')[1]"/>
      <xsl:variable name="mijnVersienummer" select="tokenize(@wId,'_')[2]"/>
      <xsl:variable name="mijneIdDeel" select="concat('__',substring-after(@wId,'__'))"/>
      <!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="matches($mijnBGcode,$BGpattern)"/>
         <xsl:otherwise>
				{"code": "STOP0146", "wId": "<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>", "BGcode": "<xsl:text/>
            <xsl:value-of select="$mijnBGcode"/>
            <xsl:text/>", "melding": "Het eerste deel van de @wId \"<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>\" heeft als BG code \"<xsl:text/>
            <xsl:value-of select="$mijnBGcode"/>
            <xsl:text/>\". Deze BG code voldoet niet aan het voorgeschreven formaat. Gebruik als BG code een aanduiding van het soort bevoegd gezag (mn, mnre, pv, gm, ws) met een volgnummer.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="matches($mijnVersienummer,$VersienummerPattern)"/>
         <xsl:otherwise>
				{"code": "STOP0147", "wId": "<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>", "Versienummer": "<xsl:text/>
            <xsl:value-of select="$mijnVersienummer"/>
            <xsl:text/>", "melding": "De @wId \"<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>\" heeft als versienummer \"<xsl:text/>
            <xsl:value-of select="$mijnVersienummer"/>
            <xsl:text/>\". Dit versienummer voldoet niet aan het voorgeschreven formaat. Gebruik als versienummer een combinatie van cijfers, onderkast- en bovenkast-letters en \"-\".", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT waarschuwing-->
      <xsl:choose>
         <xsl:when test="matches($mijneIdDeel,$eIdDeelPattern)"/>
         <xsl:otherwise>
				{"code": "STOP0148", "wId": "<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>", "eIdDeel": "<xsl:text/>
            <xsl:value-of select="$mijneIdDeel"/>
            <xsl:text/>", "melding": "Voor element met id \"<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>\" voldoet het laatste deel van de wId (\"<xsl:text/>
            <xsl:value-of select="$mijneIdDeel"/>
            <xsl:text/>\") niet aan het toegestane formaat.", "ernst": "waarschuwing"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M65"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M65"/>
   <xsl:template match="@*|node()" priority="-2" mode="M65">
      <xsl:apply-templates select="*" mode="M65"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0149@tekst-wijzigactie alleen binnen Vervang-->
   <!--RULE -->
   <xsl:template match="tekst:*[@tekst-wijzigactie][not(ancestor::tekst:Vervang)]"
                 priority="1000"
                 mode="M66">

		<!--REPORT fout-->
      <xsl:if test=".">
				{"code": "STOP0149", "element": "<xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>", "wId": "<xsl:text/>
         <xsl:value-of select="@wId"/>
         <xsl:text/>", "melding": "Het element \"<xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>\" met wId=\"<xsl:text/>
         <xsl:value-of select="@wId"/>
         <xsl:text/>\" heeft attribuut @tekst-wijzigactie. Dit is niet toegestaan buiten een tekst:Vervang. Verwijder het attribuut @tekst-wijzigactie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M66"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M66"/>
   <xsl:template match="@*|node()" priority="-2" mode="M66">
      <xsl:apply-templates select="*" mode="M66"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0150@vanParentWid alleen binnen Vervang-->
   <!--RULE -->
   <xsl:template match="tekst:*[@vanParentWid][not(ancestor::tekst:Vervang)]"
                 priority="1000"
                 mode="M67">

		<!--REPORT fout-->
      <xsl:if test=".">
				{"code": "STOP0150", "element": "<xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>", "wId": "<xsl:text/>
         <xsl:value-of select="@wId"/>
         <xsl:text/>", "melding": "Het element \"<xsl:text/>
         <xsl:value-of select="local-name()"/>
         <xsl:text/>\" met wId=\"<xsl:text/>
         <xsl:value-of select="@wId"/>
         <xsl:text/>\" heeft attribuut @vanParentWid. Dit is niet toegestaan buiten een tekst:Vervang. Verwijder het attribuut @vanParentWid.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*" mode="M67"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M67"/>
   <xsl:template match="@*|node()" priority="-2" mode="M67">
      <xsl:apply-templates select="*" mode="M67"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0151@eId-wijzigactie alleen in combinatie met wijzigactie=verplaatstNaar of verplaatsVan en binnen Proefversie-->
   <!--RULE -->
   <xsl:template match="tekst:*[@eId-wijzigactie]" priority="1000" mode="M68">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="/tekst:*[@vorm='proefversie'] and (@wijzigactie='verplaatstNaar' or @wijzigactie='verplaatstVan')"/>
         <xsl:otherwise>
				{"code": "STOP0151", "element": "<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>", "wId": "<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>", "melding": "Het element \"<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>\" met wId=\"<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>\" heeft attribuut @eId-wijzigactie. Dit atribuut is alleen toegestaan in combinatie met wijzigactie=\"verplaatstVan\" of wijzigactie=\"verplaatstNaar\" in een Proefversie. Verwijder het attribuut @eId-wijzigactie.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M68"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M68"/>
   <xsl:template match="@*|node()" priority="-2" mode="M68">
      <xsl:apply-templates select="*" mode="M68"/>
   </xsl:template>
   <!--PATTERN sch_tekst_0152@wijzigactie="verplaatstNaar" alleen binnen Proefversie-->
   <!--RULE -->
   <xsl:template match="tekst:*[@wijzigactie='verplaatstNaar']"
                 priority="1000"
                 mode="M69">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="/tekst:*[@vorm='proefversie'] and @eId-wijzigactie"/>
         <xsl:otherwise>
				{"code": "STOP0152", "element": "<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>", "wId": "<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>", "melding": "Het element \"<xsl:text/>
            <xsl:value-of select="local-name()"/>
            <xsl:text/>\" met wId=\"<xsl:text/>
            <xsl:value-of select="@wId"/>
            <xsl:text/>\" heeft attribuut @wijzigactie=\"verplaatstNaar\". Dit atribuut is alleen toegestaan in een Proefversie. Verwijder het attribuut @wijzigactie=\"verplaatstNaar\".", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*" mode="M69"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M69"/>
   <xsl:template match="@*|node()" priority="-2" mode="M69">
      <xsl:apply-templates select="*" mode="M69"/>
   </xsl:template>
</xsl:stylesheet>
