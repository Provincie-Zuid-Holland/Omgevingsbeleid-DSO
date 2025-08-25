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
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN stop_1323-->
   <!--RULE -->
   <xsl:template match="data:Procedurestap[data:soortStap = '/join/id/stop/procedure/stap_023']"
                 priority="1000"
                 mode="M4">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="data:meerInformatie"/>
         <xsl:otherwise>
        {"code": "STOP1323", "soortStap": "/join/id/stop/procedure/stap_023", "datumStap": "<xsl:text/>
            <xsl:value-of select="./data:voltooidOp"/>
            <xsl:text/>", "melding": "De stap /join/id/stop/procedure/stap_023 op datum (<xsl:text/>
            <xsl:value-of select="./data:voltooidOp"/>
            <xsl:text/>) heeft geen data:meerInformatie verwijzing. Bij deze stap is deze verwijzing verplicht. Voeg een data:meerInformatie verwijzing toe.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M4"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M4"/>
   <xsl:template match="@*|node()" priority="-2" mode="M4">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M4"/>
   </xsl:template>
   <!--PATTERN procedureverloop-->
   <!--RULE -->
   <xsl:template match="data:procedurestappen" priority="1000" mode="M5">
      <xsl:variable name="stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="data:Procedurestap">
            <xsl:sort select="normalize-space(data:soortStap/./string())"/>
            <xsl:sort select="substring(data:voltooidOp/./string(),1,10)"/>
            <xsl:variable name="code" select="normalize-space(data:soortStap/./string())"/>
            <stap>
               <code>
                  <xsl:value-of select="$code"/>
               </code>
               <datum>
                  <xsl:value-of select="substring(data:voltooidOp/./string(),1,10)"/>
               </datum>
               <xsl:choose>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_002'">
                     <uniek>1</uniek>
                     <besluit_volgorde>1</besluit_volgorde>
                     <reactie_volgorde>1</reactie_volgorde>
                     <beroep_volgorde>1</beroep_volgorde>
                     <datum_sorteervolgorde>001</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_003'">
                     <uniek>1</uniek>
                     <besluit_volgorde>2</besluit_volgorde>
                     <reactie_volgorde>1</reactie_volgorde>
                     <beroep_volgorde>1</beroep_volgorde>
                     <datum_sorteervolgorde>002</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_004'">
                     <uniek>1</uniek>
                     <besluit_volgorde>3</besluit_volgorde>
                     <datum_sorteervolgorde>003</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_014'">
                     <uniek>1</uniek>
                     <exclusief_voor_ontwerp>1</exclusief_voor_ontwerp>
                     <reactie_volgorde>2</reactie_volgorde>
                     <datum_sorteervolgorde>101</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_005'">
                     <uniek>1</uniek>
                     <exclusief_voor_ontwerp>1</exclusief_voor_ontwerp>
                     <reactie_volgorde>3</reactie_volgorde>
                     <reactie_lateredatum>1</reactie_lateredatum>
                     <datum_sorteervolgorde>102</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_015'">
                     <uniek>1</uniek>
                     <exclusief_voor_definitief>1</exclusief_voor_definitief>
                     <reactie_volgorde>2</reactie_volgorde>
                     <reactie_lateredatum>1</reactie_lateredatum>
                     <datum_sorteervolgorde>201</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_018'">
                     <uniek>1</uniek>
                     <exclusief_voor_definitief>1</exclusief_voor_definitief>
                     <beroep_volgorde>2</beroep_volgorde>
                     <in_beroep>start</in_beroep>
                     <datum_sorteervolgorde>211</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_016'">
                     <uniek>1</uniek>
                     <exclusief_voor_definitief>1</exclusief_voor_definitief>
                     <reactie_volgorde>3</reactie_volgorde>
                     <reactie_lateredatum>1</reactie_lateredatum>
                     <beroep_volgorde>3</beroep_volgorde>
                     <datum_sorteervolgorde>212</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_021'">
                     <uniek>1</uniek>
                     <exclusief_voor_definitief>1</exclusief_voor_definitief>
                     <in_beroep>einde</in_beroep>
                     <datum_sorteervolgorde>299</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_022'">
                     <uniek>1</uniek>
                     <exclusief_voor_ontwerp>1</exclusief_voor_ontwerp>
                     <besluit_volgorde>4</besluit_volgorde>
                     <besluit_lateredatum>1</besluit_lateredatum>
                     <datum_sorteervolgorde>999</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_023'">
                     <exclusief_voor_definitief>1</exclusief_voor_definitief>
                     <in_beroep>in</in_beroep>
                     <vovo>start</vovo>
                     <datum_sorteervolgorde>221</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:when test="$code = '/join/id/stop/procedure/stap_024'">
                     <exclusief_voor_definitief>1</exclusief_voor_definitief>
                     <in_beroep>in</in_beroep>
                     <vovo>einde</vovo>
                     <datum_sorteervolgorde>222</datum_sorteervolgorde>
                  </xsl:when>
                  <xsl:otherwise/>
               </xsl:choose>
            </stap>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="Beroep_ingesteld">
         <xsl:if xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="$stappen/stap[code = '/join/id/stop/procedure/stap_018']">
            <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_003'])"> 
              {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_018", "soortStap2": "/join/id/stop/procedure/stap_003", "melding": "De stap /join/id/stop/procedure/stap_003 moet vermeld worden als ook stap /join/id/stop/procedure/stap_018 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
            <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_016'])"> 
                {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_018", "soortStap2": "/join/id/stop/procedure/stap_016", "melding": "De stap /join/id/stop/procedure/stap_016 moet vermeld worden als ook stap /join/id/stop/procedure/stap_018 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
         </xsl:if>
      </xsl:variable>
      <xsl:variable name="Einde_beroepstermijn">
         <xsl:if xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="$stappen/stap[code = '/join/id/stop/procedure/stap_016']">
            <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_003'])"> 
              {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_016", "soortStap2": "/join/id/stop/procedure/stap_003", "melding": "De stap /join/id/stop/procedure/stap_003 moet vermeld worden als ook stap /join/id/stop/procedure/stap_016 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
         </xsl:if>
      </xsl:variable>
      <xsl:variable name="Begin_inzagetermijn">
         <xsl:if xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="$stappen/stap[code = '/join/id/stop/procedure/stap_014']">
            <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_005'])"> 
              {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_014", "soortStap2": "/join/id/stop/procedure/stap_005", "melding": "De stap /join/id/stop/procedure/stap_005 moet vermeld worden als ook stap /join/id/stop/procedure/stap_014 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
         </xsl:if>
      </xsl:variable>
      <xsl:variable name="Einde_bezwaar">
         <xsl:if xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="$stappen/stap[code = '/join/id/stop/procedure/stap_015']">
            <xsl:if test="not($stappen/stap[code = '/join/id/stop/procedure/stap_003'])"> 
              {"code": "STOP1319", "soortStap1": "/join/id/stop/procedure/stap_015", "soortStap2": "/join/id/stop/procedure/stap_003", "melding": "De stap /join/id/stop/procedure/stap_003 moet vermeld worden als ook stap /join/id/stop/procedure/stap_015 in het procedureverloop voorkomt.", "ernst": "fout"},</xsl:if>
         </xsl:if>
      </xsl:variable>
      <xsl:variable name="json_STOP1319"
                    select="concat($Begin_inzagetermijn,$Beroep_ingesteld,$Einde_beroepstermijn,$Einde_bezwaar)"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1319) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1319"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="json_STOP1302">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:if test="uniek = '1' and preceding-sibling::*[1]/code = code">
            {"code": "STOP1302", "soortStap": "<xsl:value-of select="code"/>", "datumStap1": "<xsl:value-of select="datum"/>", "datumStap2": "<xsl:value-of select="preceding-sibling::*[1]/datum"/>", "melding": "De stap <xsl:value-of select="code"/> komt meermalen voor, als voltooid op <xsl:value-of select="datum"/> en op <xsl:value-of select="preceding-sibling::*[1]/datum"/>.", "ernst": "fout"},</xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1302/./string()) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1302/./string()"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:sort select="datum"/>
            <xsl:sort select="number(datum_sorteervolgorde)"/>
            <xsl:choose>
               <xsl:when test="uniek = '1'">
                  <xsl:if test="not(preceding-sibling::*[1]/code) or preceding-sibling::*[1]/code != code">
                     <xsl:copy-of select="."/>
                  </xsl:if>
               </xsl:when>
               <xsl:otherwise>
                  <xsl:copy-of select="."/>
               </xsl:otherwise>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="STOP1300_exclusief_voor_ontwerp">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:if test="exclusief_voor_ontwerp = '1'">
               <xsl:value-of select="code"/>
               <xsl:text> (voltooid op </xsl:text>
               <xsl:value-of select="datum"/>
               <xsl:text>) </xsl:text>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="STOP1300_exclusief_voor_definitief">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:if test="exclusief_voor_definitief = '1'">
               <xsl:value-of select="code"/>
               <xsl:text> (voltooid op </xsl:text>
               <xsl:value-of select="datum"/>
               <xsl:text>) </xsl:text>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="not ($STOP1300_exclusief_voor_definitief != '' and $STOP1300_exclusief_voor_ontwerp != '')"/>
         <xsl:otherwise>
        {"code": "STOP1300", "soortStap1": "<xsl:text/>
            <xsl:value-of select="normalize-space($STOP1300_exclusief_voor_definitief)"/>
            <xsl:text/>", "soortStap2": "<xsl:text/>
            <xsl:value-of select="normalize-space($STOP1300_exclusief_voor_ontwerp)"/>
            <xsl:text/>", "melding": "De stappen <xsl:text/>
            <xsl:value-of select="normalize-space($STOP1300_exclusief_voor_definitief)"/>
            <xsl:text/> komen niet voor in dezelfde besluitvormingsprocedure als de stappen <xsl:text/>
            <xsl:value-of select="normalize-space($STOP1300_exclusief_voor_ontwerp)"/>
            <xsl:text/>.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="STOP1303_stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:if test="besluit_volgorde">
               <stap>
                  <code>
                     <xsl:value-of select="code"/>
                  </code>
                  <datum>
                     <xsl:value-of select="datum"/>
                  </datum>
                  <volgorde>
                     <xsl:value-of select="besluit_volgorde"/>
                  </volgorde>
                  <lateredatum>
                     <xsl:value-of select="besluit_lateredatum"/>
                  </lateredatum>
               </stap>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="json_STOP1303">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$STOP1303_stappen/stap">
            <xsl:if test="(number(preceding-sibling::*[1]/volgorde) &gt; number(volgorde) or (lateredatum != '' and datum = preceding-sibling::*[1]/datum))">
            {"code": "STOP1303", "soortStap1": "<xsl:value-of select="code"/>", "datumStap1": "<xsl:value-of select="datum"/>", "soortStap2": "<xsl:value-of select="preceding-sibling::*[1]/code"/>", "datumStap2": "<xsl:value-of select="preceding-sibling::*[1]/datum"/>", "melding": "De stap <xsl:value-of select="code"/> is voltooid op <xsl:value-of select="datum"/>, dus ná de stap <xsl:value-of select="preceding-sibling::*[1]/code"/> voltooid op datum (<xsl:value-of select="preceding-sibling::*[1]/datum"/>); terwijl de stappen in het procedureverloop in omgekeerde volgorde voorkomen.", "ernst": "fout"},</xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1303/./string()) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1303/./string()"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="STOP1304_stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:if test="reactie_volgorde">
               <stap>
                  <code>
                     <xsl:value-of select="code"/>
                  </code>
                  <datum>
                     <xsl:value-of select="datum"/>
                  </datum>
                  <volgorde>
                     <xsl:value-of select="reactie_volgorde"/>
                  </volgorde>
                  <lateredatum>
                     <xsl:value-of select="reactie_lateredatum"/>
                  </lateredatum>
               </stap>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="json_STOP1304">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$STOP1304_stappen/stap">
            <xsl:if test="(number(preceding-sibling::*[1]/volgorde) &gt; number(volgorde) or (lateredatum != '' and datum = preceding-sibling::*[1]/datum))">
            {"code": "STOP1304", "soortStap1": "<xsl:value-of select="code"/>", "datumStap1": "<xsl:value-of select="datum"/>", "soortStap2": "<xsl:value-of select="preceding-sibling::*[1]/code"/>", "datumStap2": "<xsl:value-of select="preceding-sibling::*[1]/datum"/>", "melding": "De stap <xsl:value-of select="code"/> is voltooid op <xsl:value-of select="datum"/>, dus na de stap <xsl:value-of select="preceding-sibling::*[1]/code"/> voltooid op datum (<xsl:value-of select="preceding-sibling::*[1]/datum"/>); terwijl de stappen in het procedureverloop in omgekeerde volgorde voorkomen.", "ernst": "fout"},</xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1304/./string()) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1304/./string()"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="STOP1305_stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:if test="beroep_volgorde">
               <stap>
                  <code>
                     <xsl:value-of select="code"/>
                  </code>
                  <datum>
                     <xsl:value-of select="datum"/>
                  </datum>
                  <volgorde>
                     <xsl:value-of select="beroep_volgorde"/>
                  </volgorde>
                  <lateredatum>
                     <xsl:value-of select="beroep_lateredatum"/>
                  </lateredatum>
               </stap>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="json_STOP1305">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$STOP1305_stappen/stap">
            <xsl:if test="(number(preceding-sibling::*[1]/volgorde) &gt; number(volgorde) or (lateredatum != '' and datum = preceding-sibling::*[1]/datum))">
            {"code": "STOP1305", "soortStap1": "<xsl:value-of select="code"/>", "datumStap1": "<xsl:value-of select="datum"/>", "soortStap2": "<xsl:value-of select="preceding-sibling::*[1]/code"/>", "datumStap2": "<xsl:value-of select="preceding-sibling::*[1]/datum"/>", "melding": "De stap <xsl:value-of select="code"/> is voltooid op <xsl:value-of select="datum"/>, dus na de stap <xsl:value-of select="preceding-sibling::*[1]/code"/> voltooid op datum (<xsl:value-of select="preceding-sibling::*[1]/datum"/>); terwijl de stappen in het procedureverloop in omgekeerde volgorde voorkomen.", "ernst": "fout"},</xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1305/./string()) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1305/./string()"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="STOP1310_tm_STOP1312_stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:if test="in_beroep">
               <stap>
                  <code>
                     <xsl:value-of select="code"/>
                  </code>
                  <datum>
                     <xsl:value-of select="datum"/>
                  </datum>
                  <fase>
                     <xsl:value-of select="in_beroep"/>
                  </fase>
               </stap>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="json_STOP1311">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$STOP1310_tm_STOP1312_stappen/stap">
            <xsl:choose>
               <xsl:when test="fase = 'in' and (not(preceding-sibling::*[1]/fase))">
               {"code": "STOP1311", "soortStap": "<xsl:value-of select="code"/>", "datumStap": "<xsl:value-of select="datum"/>", "melding": "De stap <xsl:value-of select="code"/> op datum (<xsl:value-of select="datum"/>) ligt niet na een 'Start beroepsprocedure'.", "ernst": "fout"},</xsl:when>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1311/./string()) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1311/./string()"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="json_STOP1312">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$STOP1310_tm_STOP1312_stappen/stap">
            <xsl:choose>
               <xsl:when test="fase = 'einde' and (preceding-sibling::*[1]/fase = 'einde' or not(preceding-sibling::*[1]/fase))">
               {"code": "STOP1312", "soortStap": "<xsl:value-of select="code"/>", "datumStap": "<xsl:value-of select="datum"/>", "melding": "De stap <xsl:value-of select="code"/> op datum (<xsl:value-of select="datum"/>) markeert het einde van een beroepsperiode, maar er is geen eerdere stap die het begin van de beroepsperiode aangeeft.", "ernst": "fout"},</xsl:when>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1312/./string()) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1312/./string()"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="STOP1313_tm_STOP1315_stappen">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$stappen/stap">
            <xsl:if test="vovo">
               <stap>
                  <code>
                     <xsl:value-of select="code"/>
                  </code>
                  <datum>
                     <xsl:value-of select="datum"/>
                  </datum>
                  <fase>
                     <xsl:value-of select="vovo"/>
                  </fase>
               </stap>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="json_STOP1313">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$STOP1313_tm_STOP1315_stappen/stap">
            <xsl:choose>
               <xsl:when test="fase = 'start' and preceding-sibling::*[1]/fase != 'einde' ">
               {"code": "STOP1313", "soortStap": "<xsl:value-of select="code"/>", "datumStap": "<xsl:value-of select="datum"/>", "melding": "De stap <xsl:value-of select="code"/> op datum (<xsl:value-of select="datum"/>) markeert het begin van een voorlopige voorzieningen periode, maar de voorgaande periode is nog niet afgesloten.", "ernst": "fout"},</xsl:when>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1313/./string()) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1313/./string()"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="json_STOP1315">
         <xsl:for-each xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$STOP1313_tm_STOP1315_stappen/stap">
            <xsl:choose>
               <xsl:when test="fase = 'einde' and (preceding-sibling::*[1]/fase != 'start' or not(preceding-sibling::*[1]/fase))">
               {"code": "STOP1315", "soortStap": "<xsl:value-of select="code"/>", "datumStap": "<xsl:value-of select="datum"/>", "melding": "De stap <xsl:value-of select="code"/> op datum (<xsl:value-of select="datum"/>) markeert het einde van een voorlopige voorzieningen periode, maar er is geen eerdere stap die het begin van deze periode aangeeft.", "ernst": "fout"},</xsl:when>
            </xsl:choose>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($json_STOP1315/./string()) = ''"/>
         <xsl:otherwise>
            <xsl:text/>
            <xsl:value-of select="$json_STOP1315/./string()"/>
            <xsl:text/>
            <xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M5"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M5"/>
   <xsl:template match="@*|node()" priority="-2" mode="M5">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M5"/>
   </xsl:template>
</xsl:stylesheet>
