<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<xsl:stylesheet xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:saxon="http://saxon.sf.net/"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:schold="http://www.ascc.net/xml/schematron"
                xmlns:iso="http://purl.oclc.org/dsdl/schematron"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                xmlns:geo="https://standaarden.overheid.nl/stop/imop/geo/"
                xmlns:basisgeo="http://www.geostandaarden.nl/basisgeometrie/1.0"
                xmlns:gml="http://www.opengis.net/gml/3.2"
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
      <xsl:apply-templates select="/" mode="M6"/>
      <xsl:apply-templates select="/" mode="M7"/>
      <xsl:apply-templates select="/" mode="M8"/>
      <xsl:apply-templates select="/" mode="M9"/>
      <xsl:apply-templates select="/" mode="M10"/>
      <xsl:apply-templates select="/" mode="M11"/>
      <xsl:apply-templates select="/" mode="M12"/>
      <xsl:apply-templates select="/" mode="M13"/>
      <xsl:apply-templates select="/" mode="M14"/>
      <xsl:apply-templates select="/" mode="M15"/>
      <xsl:apply-templates select="/" mode="M16"/>
      <xsl:apply-templates select="/" mode="M17"/>
      <xsl:apply-templates select="/" mode="M18"/>
      <xsl:apply-templates select="/" mode="M19"/>
      <xsl:apply-templates select="/" mode="M20"/>
      <xsl:apply-templates select="/" mode="M21"/>
      <xsl:apply-templates select="/" mode="M22"/>
      <xsl:apply-templates select="/" mode="M23"/>
      <xsl:apply-templates select="/" mode="M24"/>
   </xsl:template>
   <!--SCHEMATRON PATTERNS-->
   <!--PATTERN sch_geo_001Locatie rules voor GIO-versie of GIO-mutatie-->
   <!--RULE -->
   <xsl:template match="geo:locaties | geo:locatieMutaties"
                 priority="1000"
                 mode="M6">
      <xsl:variable name="aantalLocaties"
                    select="count(./geo:Locatie) + count(./geo:LocatieMutatie)"/>
      <xsl:variable name="aantalLocatiesMetGroepID"
                    select="count(./geo:Locatie/geo:groepID) + count(./geo:LocatieMutatie/geo:groepID)"/>
      <xsl:variable name="aantalLocatiesMetKwantitatieveNormwaarde"
                    select="count(./geo:Locatie/geo:kwantitatieveNormwaarde) + count(./geo:LocatieMutatie/geo:kwantitatieveNormwaarde)"/>
      <xsl:variable name="aantalLocatiesMetKwalitatieveNormwaarde"
                    select="count(./geo:Locatie/geo:kwalitatieveNormwaarde) + count(./geo:LocatieMutatie/geo:kwalitatieveNormwaarde)"/>
      <xsl:variable name="Expressie"
                    select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="($aantalLocatiesMetGroepID = 0) or ($aantalLocatiesMetGroepID = $aantalLocaties)"/>
         <xsl:otherwise>
				{"code": "STOP3000", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="$Expressie"/>
            <xsl:text/>", "melding": "Als er 1 locatie is in een GIO waar een waarde groepID is ingevuld moet elke locatie een GroepID hebben. Geef alle locaties een groepID (GIO <xsl:text/>
            <xsl:value-of select="$Expressie"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="($aantalLocatiesMetKwantitatieveNormwaarde = 0) or ($aantalLocatiesMetKwantitatieveNormwaarde = $aantalLocaties)"/>
         <xsl:otherwise>
				{"code": "STOP3006", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="$Expressie"/>
            <xsl:text/>", "melding": "Een locatie heeft een kwantitatieveNormwaarde, en één of meerdere andere locaties niet. Geef alle locaties een kwantitatieveNormwaarde, of verwijder alle kwantitatieveNormwaardes (GIO <xsl:text/>
            <xsl:value-of select="$Expressie"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="($aantalLocatiesMetKwalitatieveNormwaarde = 0) or ($aantalLocatiesMetKwalitatieveNormwaarde = $aantalLocaties)"/>
         <xsl:otherwise>
				{"code": "STOP3007", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="$Expressie"/>
            <xsl:text/>", "melding": "Een locatie heeft een kwalitatieveNormwaarde, en één of meerdere andere locaties niet. Geef alle locaties een kwalitatieveNormwaarde, of verwijder alle kwalitatieveNormwaardes (GIO <xsl:text/>
            <xsl:value-of select="$Expressie"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--REPORT fout-->
      <xsl:if test="(($aantalLocatiesMetKwantitatieveNormwaarde gt 0) and ((not(exists(../geo:eenheidlabel))) or (not(exists(../geo:eenheidID)))))">
				{"code": "STOP3009", "ExpressieID": "<xsl:text/>
         <xsl:value-of select="$Expressie"/>
         <xsl:text/>", "melding": "De locaties bevatten kwantitatieve normwaarden, terwijl eenheidlabel en/of eenheidID ontbreken. Vul deze aan (GIO <xsl:text/>
         <xsl:value-of select="$Expressie"/>
         <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="(($aantalLocatiesMetKwalitatieveNormwaarde gt 0) and ((exists(../geo:eenheidlabel) or exists(../geo:eenheidID))))">
				{"code": "STOP3015", "ExpressieID": "<xsl:text/>
         <xsl:value-of select="$Expressie"/>
         <xsl:text/>", "melding": "Het GIO met kwalitatieve normwaarden mag geen eenheidlabel noch eenheidID hebben. Verwijder eenheidlabel en eenheidID toe, of verander de kwalitatieve in kwantitatieve normwaarden (GIO <xsl:text/>
         <xsl:value-of select="$Expressie"/>
         <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <!--REPORT fout-->
      <xsl:if test="((($aantalLocatiesMetKwantitatieveNormwaarde + $aantalLocatiesMetKwalitatieveNormwaarde) gt 0) and ((not(exists(../geo:normlabel))) or (not(exists(../geo:normID)))))">
				{"code": "STOP3011", "ExpressieID": "<xsl:text/>
         <xsl:value-of select="$Expressie"/>
         <xsl:text/>", "melding": "De locaties bevatten wel kwantitatieve òf kwalitatieve normwaarden, maar geen norm. Vul normlabel en normID aan (GIO <xsl:text/>
         <xsl:value-of select="$Expressie"/>
         <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M6"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M6"/>
   <xsl:template match="@*|node()" priority="-2" mode="M6">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M6"/>
   </xsl:template>
   <!--PATTERN sch_geo_3013-->
   <!--RULE -->
   <xsl:template match="geo:locaties" priority="1000" mode="M7">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(./geo:Locatie/geo:geometrie/basisgeo:Geometrie/basisgeo:id) = count(distinct-values(./geo:Locatie/geo:geometrie/basisgeo:Geometrie/basisgeo:id))"/>
         <xsl:otherwise>
				{"code": "STOP3013", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <xsl:text/>", "melding": "De basisgeo:id's van de locaties zijn niet uniek. Binnen 1 GIO-versie mag basisgeo:id van geometrische objecten van verschillende locaties niet gelijk zijn aan elkaar. Pas dit aan (GIO <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M7"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M7"/>
   <xsl:template match="@*|node()" priority="-2" mode="M7">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M7"/>
   </xsl:template>
   <!--PATTERN sch_geo_3032-->
   <!--RULE -->
   <xsl:template match="geo:locatieMutaties" priority="1000" mode="M8">
      <xsl:variable name="voegtoe"
                    select="count(geo:LocatieMutatie[geo:wijzigactie='voegtoe' or geo:wijzigactie='reviseer']/geo:geometrie/basisgeo:Geometrie/basisgeo:id)"/>
      <xsl:variable name="voegtoeDis"
                    select="count(distinct-values(geo:LocatieMutatie[geo:wijzigactie='voegtoe' or geo:wijzigactie='reviseer']/geo:geometrie/basisgeo:Geometrie/basisgeo:id))"/>
      <xsl:variable name="verwijder"
                    select="count(geo:LocatieMutatie[geo:wijzigactie='verwijder' or geo:wijzigactie='reviseer']/geo:geometrie/basisgeo:Geometrie/basisgeo:id)"/>
      <xsl:variable name="verwijderDis"
                    select="count(distinct-values(geo:LocatieMutatie[geo:wijzigactie='verwijder' or geo:wijzigactie='reviseer']/geo:geometrie/basisgeo:Geometrie/basisgeo:id))"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="$voegtoe = $voegtoeDis and $verwijder = $verwijderDis"/>
         <xsl:otherwise>
				{"code": "STOP3032", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>", "melding": "De geo:locatieMutaties leiden tot niet unieke basisgeo:id's van de locaties in de nieuwe GIO-versie. Binnen 1 GIO-versie mogen de basisgeo:id's van geometrische objecten van verschillende locaties niet gelijk zijn aan elkaar. Pas dit aan (GIO <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M8"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M8"/>
   <xsl:template match="@*|node()" priority="-2" mode="M8">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M8"/>
   </xsl:template>
   <!--PATTERN sch_geo_3034-->
   <!--RULE -->
   <xsl:template match="geo:wijzigmarkeringen" priority="1000" mode="M9">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(.//geo:geometrie/basisgeo:Geometrie/basisgeo:id) = count(distinct-values(.//geo:geometrie/basisgeo:Geometrie/basisgeo:id))"/>
         <xsl:otherwise>
				{"code": "STOP3034", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>", "melding": "De basisgeo:id's van de geometrieen in de geo:wijzigmarkeringen zijn niet uniek. Omdat de wijzigmarkeringen elkaar niet mogen overlappen, mogen de basisgeo:id's van geometrische objecten niet gelijk zijn aan elkaar. Pas dit aan (GIO <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M9"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M9"/>
   <xsl:template match="@*|node()" priority="-2" mode="M9">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M9"/>
   </xsl:template>
   <!--PATTERN sch_geo_3008-->
   <!--RULE -->
   <xsl:template match="geo:Locatie | geo:LocatieMutatie" priority="1000" mode="M10">
      <xsl:variable name="ID" select="geo:geometrie/basisgeo:Geometrie/basisgeo:id"/>
      <xsl:variable name="Expressie"
                    select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(geo:kwantitatieveNormwaarde) + count(geo:kwalitatieveNormwaarde) le 1"/>
         <xsl:otherwise>
				{"code": "STOP3008", "ID": "<xsl:text/>
            <xsl:value-of select="$ID"/>
            <xsl:text/>", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="$Expressie"/>
            <xsl:text/>", "melding": "Locatie met basisgeo:id <xsl:text/>
            <xsl:value-of select="$ID"/>
            <xsl:text/> heeft zowel een kwalitatieveNormwaarde als een kwantitatieveNormwaarde. Verwijder één van beide (GIO <xsl:text/>
            <xsl:value-of select="$Expressie"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <!--REPORT fout-->
      <xsl:if test="exists(geo:groepID) and (exists(geo:kwalitatieveNormwaarde) or exists(geo:kwantitatieveNormwaarde))">
				{"code": "STOP3012", "ID": "<xsl:text/>
         <xsl:value-of select="$ID"/>
         <xsl:text/>", "ExpressieID": "<xsl:text/>
         <xsl:value-of select="$Expressie"/>
         <xsl:text/>", "melding": "Locatie met basisgeo:id <xsl:text/>
         <xsl:value-of select="$ID"/>
         <xsl:text/> heeft zowel een groepID (GIO-deel) als een (kwalitatieve of kwantitatieve) Normwaarde. Verwijder de Normwaarde of de groepID (GIO <xsl:text/>
         <xsl:value-of select="$Expressie"/>
         <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M10"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M10"/>
   <xsl:template match="@*|node()" priority="-2" mode="M10">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M10"/>
   </xsl:template>
   <!--PATTERN sch_geo_3010-->
   <!--RULE -->
   <xsl:template match="geo:kwalitatieveNormwaarde" priority="1000" mode="M11">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space(.)"/>
         <xsl:otherwise>
				{"code": "STOP3010", "ID": "<xsl:text/>
            <xsl:value-of select="../geo:geometrie/basisgeo:Geometrie/basisgeo:id"/>
            <xsl:text/>", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>", "melding": "De kwalitatieveNormwaarde van locatie met basisgeo:id <xsl:text/>
            <xsl:value-of select="../geo:geometrie/basisgeo:Geometrie/basisgeo:id"/>
            <xsl:text/> is niet gevuld. Vul deze aan (GIO <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M11"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M11"/>
   <xsl:template match="@*|node()" priority="-2" mode="M11">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M11"/>
   </xsl:template>
   <!--PATTERN sch_geo_002
			Als een locatie een groepID heeft, dan MOET deze voorkomen in het lijstje
			groepen.
		-->
   <!--RULE -->
   <xsl:template match="geo:Locatie/geo:groepID | geo:LocatieMutatie/geo:groepID"
                 priority="1000"
                 mode="M12">
      <xsl:variable name="doelwit" select="./string()"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(../../../geo:groepen/geo:Groep[geo:groepID = $doelwit]) gt 0"/>
         <xsl:otherwise>
				{"code": "STOP3001", "ID": "<xsl:text/>
            <xsl:value-of select="$doelwit"/>
            <xsl:text/>", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>", "melding": "Als een locatie een groepID heeft, dan MOET deze voorkomen in het lijstje groepen. GroepID <xsl:text/>
            <xsl:value-of select="$doelwit"/>
            <xsl:text/> komt niet voor in groepen. Geef alle locaties een groepID die voorkomt in groepen (GIO <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M12"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M12"/>
   <xsl:template match="@*|node()" priority="-2" mode="M12">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M12"/>
   </xsl:template>
   <!--PATTERN sch_geo_004Check op unieke labels en groepIDs.-->
   <!--RULE -->
   <xsl:template match="geo:groepen" priority="1000" mode="M13">
      <xsl:variable name="GroepIDs">
         <xsl:for-each xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                       xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="geo:Groep">
            <xsl:sort select="normalize-space(geo:groepID/./string())"/>
            <ID>
               <xsl:value-of select="geo:groepID/string()"/>
            </ID>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="DubbeleGroepen">
         <xsl:for-each xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                       xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$GroepIDs/ID">
            <xsl:if test="preceding::ID[1] = .">
               <dubbel>
							(<xsl:value-of select="./string()"/>, <xsl:value-of select="preceding::ID[1]/string()"/>)
						</dubbel>
               <xsl:text> </xsl:text>
            </xsl:if>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($DubbeleGroepen) = ''"/>
         <xsl:otherwise>
				{"code": "STOP3003", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>", "Dubbel": "<xsl:text/>
            <xsl:value-of select="$DubbeleGroepen/normalize-space()"/>
            <xsl:text/>", "melding": "GroepID <xsl:text/>
            <xsl:value-of select="$DubbeleGroepen/normalize-space()"/>
            <xsl:text/> komt meerdere keren voor. Zorg dat iedere Groep een uniek ID heeft (GIO <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:variable name="Labels">
         <xsl:for-each xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                       xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="geo:Groep">
            <xsl:sort select="normalize-space(geo:label/./string())"/>
            <naam>
               <xsl:value-of select="geo:label"/>
            </naam>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="DubbeleLabels">
         <xsl:for-each xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                       xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select="$Labels/naam">
            <xsl:if test="preceding::naam[1] = .">
						(<xsl:value-of select="./string()"/>, <xsl:value-of select="preceding::naam[1]/string()"/>)
					</xsl:if>
            <xsl:text> </xsl:text>
         </xsl:for-each>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="normalize-space($DubbeleLabels) = ''"/>
         <xsl:otherwise>
				{"code": "STOP3004", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>", "Dubbel": "<xsl:text/>
            <xsl:value-of select="$DubbeleLabels/normalize-space()"/>
            <xsl:text/>", "melding": "Het label <xsl:text/>
            <xsl:value-of select="$DubbeleLabels/normalize-space()"/>
            <xsl:text/> meerdere keren voor in het lijstje met groepen. Geef unieke labels. (GIO <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>)", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M13"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M13"/>
   <xsl:template match="@*|node()" priority="-2" mode="M13">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M13"/>
   </xsl:template>
   <!--PATTERN sch_geo_005
			Als een groepID voorkomt in het lijstje groepen dan MOET er minstens 1 locatie zijn
			met dat groepID.
		-->
   <!--RULE -->
   <xsl:template match="geo:groepen/geo:Groep/geo:groepID"
                 priority="1000"
                 mode="M14">
      <xsl:variable name="doelwit" select="./string()"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(../../../geo:locaties/geo:Locatie[./geo:groepID = $doelwit]) gt 0 or count(../../../geo:locatieMutaties/geo:LocatieMutatie[./geo:groepID = $doelwit]) gt 0"/>
         <xsl:otherwise>
				{"code": "STOP3005", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>", "ID": "<xsl:text/>
            <xsl:value-of select="$doelwit"/>
            <xsl:text/>", "melding": "GroepID <xsl:text/>
            <xsl:value-of select="$doelwit"/>
            <xsl:text/> wordt niet gebruikt voor een locatie. Verwijder deze groep, of gebruik de groep bij een Locatie (GIO <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M14"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M14"/>
   <xsl:template match="@*|node()" priority="-2" mode="M14">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M14"/>
   </xsl:template>
   <!--PATTERN sch_geo_006Geen norm elementen in een GIO zonder normwaarde.-->
   <!--RULE -->
   <xsl:template match="geo:GeoInformatieObjectVersie | geo:GeoInformatieObjectMutatie"
                 priority="1000"
                 mode="M15">

		<!--REPORT fout-->
      <xsl:if test="(exists(geo:normID) or exists(geo:normlabel) or exists(geo:eenheidID) or exists(geo:eenheidlabel)) and (count(geo:locaties/geo:Locatie/geo:kwantitatieveNormwaarde) = 0 and count(geo:locaties/geo:Locatie/geo:kwalitatieveNormwaarde) = 0) and (count(geo:locatieMutaties/geo:LocatieMutatie/geo:kwantitatieveNormwaarde) = 0 and count(geo:locatieMutaties/geo:LocatieMutatie/geo:kwalitatieveNormwaarde) = 0)">
				{"code": "STOP3016", "ExpressieID": "<xsl:text/>
         <xsl:value-of select="geo:FRBRExpression"/>
         <xsl:text/>", "melding": "Het GIO bevat norm (normID en normlabel) en/of eenheid (eenheidID en eenheidlabel), terwijl kwantitatieve of kwalitatieve normwaarden ontbreken. Geef de locaties normwaarden of verwijder de norm/eenheid-elementen (GIO <xsl:text/>
         <xsl:value-of select="geo:FRBRExpression"/>
         <xsl:text/>).", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M15"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M15"/>
   <xsl:template match="@*|node()" priority="-2" mode="M15">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M15"/>
   </xsl:template>
   <!--PATTERN sch_basisgeo_001
			Locaties in een GIO MOETEN een geometrie hebben. (basisgeo:geometrie in
			basisgeo:Geometrie MAG NIET ontbreken of leeg zijn).
		-->
   <!--RULE -->
   <xsl:template match="basisgeo:geometrie" priority="1000" mode="M16">
      <xsl:variable name="coordinaten">
         <xsl:for-each xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                       xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                       xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                       select=".//gml:posList | .//gml:pos | .//gml:coordinates">
            <xsl:value-of select="./string()"/>
            <xsl:text> </xsl:text>
         </xsl:for-each>
      </xsl:variable>
      <xsl:variable name="kenmerk">
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(../../..) = 'geo:Locatie'">(naam='<xsl:value-of select="ancestor::geo:Locatie/geo:naam"/>') in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression"/>'</xsl:if>
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(../../..) = 'geo:LocatieMutatie'">(naam='<xsl:value-of select="ancestor::geo:LocatieMutatie/geo:naam"/>') in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>'</xsl:if>
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(../../..) = 'geo:Punt'">(punt in wijzigmarkering) in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>'</xsl:if>
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(../../..) = 'geo:Lijn'">(lijn in wijzigmarkering) in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>'</xsl:if>
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(../../..) = 'geo:Vlak'">(vlak in wijzigmarkering) in GIO met FRBRExpressie='<xsl:value-of select="ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>'</xsl:if>
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(../../..) = 'geo:Gebied'">(label='<xsl:value-of select="ancestor::geo:Gebied/geo:label"/>')</xsl:if>
      </xsl:variable>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="(descendant::gml:pos or descendant::gml:posList or descendant::gml:coordinates) and matches($coordinaten, '\d')"/>
         <xsl:otherwise>
				{"code": "STOP3019", "basisgeo:id": "<xsl:text/>
            <xsl:value-of select="preceding-sibling::basisgeo:id"/>
            <xsl:text/>", "Parent": "<xsl:text/>
            <xsl:value-of select="node-name(../../..)"/>
            <xsl:text/>", "Kenmerk": "<xsl:text/>
            <xsl:value-of select="$kenmerk"/>
            <xsl:text/>", "melding": "<xsl:text/>
            <xsl:value-of select="node-name(../../..)"/>
            <xsl:text/>
            <xsl:text/>
            <xsl:value-of select="$kenmerk"/>
            <xsl:text/> met basisgeo:geometrie (<xsl:text/>
            <xsl:value-of select="preceding-sibling::basisgeo:id"/>
            <xsl:text/>) heeft geen of een lege geometrie. Basisgeo:Geometrie zonder geometrische data is niet toegestaan. Voeg een (correcte) basisgeo:geometrie toe.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M16"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M16"/>
   <xsl:template match="@*|node()" priority="-2" mode="M16">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M16"/>
   </xsl:template>
   <!--PATTERN sch_gml_001
			Coördinaten in geometrieen in een GIO MOETEN gebruik maken van het RD of ETRS89
			ruimtelijke referentiesysteem(srsName='urn:ogc:def:crs:EPSG::28992' of
			srsName='urn:ogc:def:crs:EPSG::4258').
		-->
   <!--RULE -->
   <xsl:template match="geo:locaties//gml:*[@srsName] | geo:locatieMutaties//gml:*[@srsName] | geo:wijzigmarkeringen//gml:*[@srsName]"
                 priority="1000"
                 mode="M17">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="@srsName = 'urn:ogc:def:crs:EPSG::28992' or @srsName = 'urn:ogc:def:crs:EPSG::4258'"/>
         <xsl:otherwise>
				{"code": "STOP3020", "srsName": "<xsl:text/>
            <xsl:value-of select="@srsName"/>
            <xsl:text/>", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>", "melding": "Het GIO (<xsl:text/>
            <xsl:value-of select="ancestor::geo:GeoInformatieObjectVersie/geo:FRBRExpression | ancestor::geo:GeoInformatieObjectMutatie/geo:FRBRExpression"/>
            <xsl:text/>) bevat een geometrisch object met een ongeldige srsName (<xsl:text/>
            <xsl:value-of select="@srsName"/>
            <xsl:text/>). Alleen srsName='urn:ogc:def:crs:EPSG::28992' of srsName='urn:ogc:def:crs:EPSG::4258' is toegestaan. Wijzig de srsName.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M17"/>
   <xsl:template match="@*|node()" priority="-2" mode="M17">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M17"/>
   </xsl:template>
   <!--PATTERN sch_gml_3021Alle srsNames identiek-->
   <!--RULE -->
   <xsl:template match="geo:GeoInformatieObjectVersie | geo:GeoInformatieObjectMutatie"
                 priority="1000"
                 mode="M18">
      <xsl:variable name="srsName" select="//@srsName"/>
      <!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="count(distinct-values(//@srsName)) = 1"/>
         <xsl:otherwise>
				{"code": "STOP3021", "srsNames": "<xsl:text/>
            <xsl:value-of select="distinct-values($srsName)"/>
            <xsl:text/>", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="geo:FRBRExpression"/>
            <xsl:text/>", "melding": "In GIO (<xsl:text/>
            <xsl:value-of select="geo:FRBRExpression"/>
            <xsl:text/>) heeft niet elk geometrisch object dezelfde srsName (<xsl:text/>
            <xsl:value-of select="distinct-values($srsName)"/>
            <xsl:text/>). Dit is niet toegestaan. Zorg ervoor dat elke geometrisch object in het GIO hetzelfde ruimtelijke referentiesysteem (srsName) gebruikt.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M18"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M18"/>
   <xsl:template match="@*|node()" priority="-2" mode="M18">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M18"/>
   </xsl:template>
   <!--PATTERN sch_gml_3040Geen cirkels en bogen in de basisgeometrie-->
   <!--RULE -->
   <xsl:template match="basisgeo:Geometrie//gml:Circle | basisgeo:Geometrie//gml:Arc | basisgeo:Geometrie//gml:CircleByCenterPoint"
                 priority="1000"
                 mode="M19">

		<!--REPORT fout-->
      <xsl:if test=".">
				{"code": "STOP3040", "Element": "<xsl:text/>
         <xsl:value-of select="string(node-name(.))"/>
         <xsl:text/>", "id": "<xsl:text/>
         <xsl:value-of select="ancestor::basisgeo:Geometrie/basisgeo:id"/>
         <xsl:text/>", "melding": "De basisgeo:Geometrie(basisgeo:id <xsl:text/>
         <xsl:value-of select="ancestor::basisgeo:Geometrie/basisgeo:id"/>
         <xsl:text/>) bevat een gml aanduiding voor een cirkel of boog (<xsl:text/>
         <xsl:value-of select="string(node-name(.))"/>
         <xsl:text/>). Dit is niet toegestaan. Verwijder <xsl:text/>
         <xsl:value-of select="string(node-name(.))"/>
         <xsl:text/>.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M19"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M19"/>
   <xsl:template match="@*|node()" priority="-2" mode="M19">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M19"/>
   </xsl:template>
   <!--PATTERN sch_gml_3050
			Coördinaten in geometrieen in een geo:Gebied MOETEN gebruik maken van het RD
			ruimtelijke referentiesysteem(srsName='urn:ogc:def:crs:EPSG::28992').
		-->
   <!--RULE -->
   <xsl:template match="geo:Gebied//gml:*[@srsName]" priority="1000" mode="M20">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="@srsName = 'urn:ogc:def:crs:EPSG::28992'"/>
         <xsl:otherwise>
				{"code": "STOP3050", "srsName": "<xsl:text/>
            <xsl:value-of select="@srsName"/>
            <xsl:text/>", "label": "<xsl:text/>
            <xsl:value-of select="ancestor::geo:Gebied/geo:label"/>
            <xsl:text/>", "melding": "geo:Gebied(label: <xsl:text/>
            <xsl:value-of select="ancestor::geo:Gebied/geo:label"/>
            <xsl:text/>) bevat een geometrisch object met een ongeldige srsName (<xsl:text/>
            <xsl:value-of select="@srsName"/>
            <xsl:text/>). Alleen srsName='urn:ogc:def:crs:EPSG::28992' is toegestaan. Wijzig de srsName.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M20"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M20"/>
   <xsl:template match="@*|node()" priority="-2" mode="M20">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M20"/>
   </xsl:template>
   <!--PATTERN sch_gml_3060Effectgebied bevat een vlak in de basisgeometrie-->
   <!--RULE -->
   <xsl:template match="basisgeo:geometrie[ancestor::geo:Effectgebied]"
                 priority="1000"
                 mode="M21">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test=".//gml:Surface or .//gml:Polygon"/>
         <xsl:otherwise>
				{"code": "STOP3060", "Element": "<xsl:text/>
            <xsl:value-of select="string(node-name(./gml:*))"/>
            <xsl:text/>", "label": "<xsl:text/>
            <xsl:value-of select="string(ancestor::geo:Gebied/geo:label)"/>
            <xsl:text/>", "id": "<xsl:text/>
            <xsl:value-of select="string(ancestor::basisgeo:Geometrie/basisgeo:id)"/>
            <xsl:text/>", "melding": "Het Effectgebied met geo:label='<xsl:text/>
            <xsl:value-of select="string(ancestor::geo:Gebied/geo:label)"/>
            <xsl:text/>' bevat een basisgeo:Geometrie(id=<xsl:text/>
            <xsl:value-of select="string(ancestor::basisgeo:Geometrie/basisgeo:id)"/>
            <xsl:text/>) met gml aanduiding (<xsl:text/>
            <xsl:value-of select="string(node-name(./gml:*))"/>
            <xsl:text/>) in plaats van een gml aanduiding voor een vlak. Dit is niet toegestaan. Vervang <xsl:text/>
            <xsl:value-of select="string(node-name(./gml:*))"/>
            <xsl:text/> door gml:Surface of gml:Polygon.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M21"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M21"/>
   <xsl:template match="@*|node()" priority="-2" mode="M21">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M21"/>
   </xsl:template>
   <!--PATTERN sch_gml_3065Gebiedsmarkering bevat òf ambtsgebied òf een of meer gebied-en-->
   <!--RULE -->
   <xsl:template match="geo:Gebiedsmarkering" priority="1000" mode="M22">

		<!--REPORT fout-->
      <xsl:if test="geo:Gebied and geo:Ambtsgebied">
				{"code": "STOP3065", "bgCode": "<xsl:text/>
         <xsl:value-of select="string(geo:Ambtsgebied/geo:bevoegdGezag)"/>
         <xsl:text/>", "aantal": "<xsl:text/>
         <xsl:value-of select="string(count(child::geo:Gebied))"/>
         <xsl:text/>", "label": "<xsl:text/>
         <xsl:value-of select="string(child::geo:Gebied[1]/geo:label)"/>
         <xsl:text/>", "melding": "Gebiedsmarkering bevat een combinatie van geo:Ambtsgebied (met geo:bevoegdGezag <xsl:text/>
         <xsl:value-of select="string(geo:Ambtsgebied/geo:bevoegdGezag)"/>
         <xsl:text/>) en <xsl:text/>
         <xsl:value-of select="string(count(child::geo:Gebied))"/>
         <xsl:text/>x geo:Gebied (eerste gebied heeft geo:label='<xsl:text/>
         <xsl:value-of select="string(child::geo:Gebied[1]/geo:label)"/>
         <xsl:text/>'). Dit is niet toegestaan. Verwijder òf het geo:Ambtsgebied òf ALLE geo:Gebied-en.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M22"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M22"/>
   <xsl:template match="@*|node()" priority="-2" mode="M22">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M22"/>
   </xsl:template>
   <!--PATTERN sch_gml_3080Een GIO-mutatie MOET een was-ID verwijzing hebben.-->
   <!--RULE -->
   <xsl:template match="geo:GeoInformatieObjectVaststelling/geo:vastgesteldeVersie/geo:GeoInformatieObjectMutatie"
                 priority="1000"
                 mode="M23">

		<!--ASSERT fout-->
      <xsl:choose>
         <xsl:when test="ancestor::geo:GeoInformatieObjectVaststelling/geo:wasID"/>
         <xsl:otherwise>
				{"code": "STOP3080", "ExpressieID": "<xsl:text/>
            <xsl:value-of select="geo:FRBRExpression"/>
            <xsl:text/>", "melding": "De was-ID verwijzing ontbreekt in GIO <xsl:text/>
            <xsl:value-of select="geo:FRBRExpression"/>
            <xsl:text/>. Het GIO bevat GIO-wijzigingen waardoor een was-ID verwijzing verplicht is. Voeg de was-ID toe.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
         </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M23"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M23"/>
   <xsl:template match="@*|node()" priority="-2" mode="M23">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M23"/>
   </xsl:template>
   <!--PATTERN sch_gml_03090Geen optionele gml AbstractFeatureType elementen in de geo: namespace-->
   <!--RULE -->
   <xsl:template match="gml:metaDataProperty[parent::geo:*] | gml:description[parent::geo:*] | gml:descriptionReference[parent::geo:*] | gml:identifier[parent::geo:*] | gml:name[parent::geo:*] | gml:boundedBy[parent::geo:*] | gml:location[parent::geo:*] | gml:PriorityLocation[parent::geo:*]"
                 priority="1000"
                 mode="M24">
      <xsl:variable name="kenmerk">
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(..) = 'geo:GeoInformatieObjectVaststelling' or name(..) = 'geo:GeoInformatieObjectVersie' or name(..) = 'geo:GeoInformatieObjectMutatie'"> binnen GIO met FRBRExpressie '<xsl:value-of select="../descendant::geo:FRBRExpression"/>'</xsl:if>
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(..) = 'geo:Locatie'"> met naam '<xsl:value-of select="../geo:naam"/>'</xsl:if>
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(..) = 'geo:LocatieMutatie'"> met naam '<xsl:value-of select="../geo:naam"/>'</xsl:if>
         <xsl:if xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
                 xmlns:sch="http://purl.oclc.org/dsdl/schematron"
                 xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
                 test="name(..) = 'geo:Gebied'"> met label '<xsl:value-of select="../geo:label"/>'</xsl:if>
      </xsl:variable>
      <!--REPORT fout-->
      <xsl:if test=".">
				{"code": "STOP3090", "Kenmerk": "<xsl:text/>
         <xsl:value-of select="$kenmerk"/>
         <xsl:text/>", "Element": "<xsl:text/>
         <xsl:value-of select="string(node-name(.))"/>
         <xsl:text/>", "Parent": "<xsl:text/>
         <xsl:value-of select="string(node-name(..))"/>
         <xsl:text/>", "melding": "<xsl:text/>
         <xsl:value-of select="string(node-name(..))"/>
         <xsl:text/>
         <xsl:text/>
         <xsl:value-of select="$kenmerk"/>
         <xsl:text/> bevat het optionele gml-element <xsl:text/>
         <xsl:value-of select="string(node-name(.))"/>
         <xsl:text/>. Dit element mag niet worden gebruikt in een GIO. Verwijder dit element.", "ernst": "fout"},<xsl:value-of select="string('&#xA;')"/>
      </xsl:if>
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M24"/>
   </xsl:template>
   <xsl:template match="text()" priority="-1" mode="M24"/>
   <xsl:template match="@*|node()" priority="-2" mode="M24">
      <xsl:apply-templates select="*|comment()|processing-instruction()" mode="M24"/>
   </xsl:template>
</xsl:stylesheet>
