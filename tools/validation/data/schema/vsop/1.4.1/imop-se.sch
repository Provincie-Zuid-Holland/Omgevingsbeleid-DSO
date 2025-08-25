<?xml version="1.0" encoding="UTF-8"?>
<sch:schema xmlns:data="https://standaarden.overheid.nl/stop/imop/data/"
            xmlns:sch="http://purl.oclc.org/dsdl/schematron"
            xmlns:se="http://www.opengis.net/se"
            xmlns:sqf="http://www.schematron-quickfix.com/validator/process"
            xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
            queryBinding="xslt2">
   <sch:ns prefix="geo" uri="https://standaarden.overheid.nl/stop/imop/geo/"/>
   <sch:ns prefix="se" uri="http://www.opengis.net/se"/>
   <sch:ns prefix="ogc" uri="http://www.opengis.net/ogc"/>
   <sch:ns prefix="xsl" uri="http://www.w3.org/1999/XSL/Transform"/>
   <sch:ns prefix="basisgeo" uri="http://www.geostandaarden.nl/basisgeometrie/1.0"/>
   <sch:ns prefix="gml" uri="http://www.opengis.net/gml/3.2"/>
   <sch:p>Versie 1.4.1</sch:p>
   <sch:p>Schematron voor aanvullende validatie voor het STOP-deel van de Symbol Encoding (se)
    standaard.</sch:p>
   <sch:pattern id="sch_se_001" see="se:FeatureTypeStyle">
      <sch:rule context="se:FeatureTypeStyle">
         <sch:assert id="STOP3100" test="not(se:Name)" role="waarschuwing">
        {"code": "STOP3100", "ID": "<sch:value-of select="./se:Name"/>", "melding": "De FeatureTypeStyle bevat een Name <sch:value-of select="./se:Name"/>, deze informatie wordt genegeerd.", "ernst": "waarschuwing"},</sch:assert>
         <sch:assert id="STOP3101" test="not(se:Description)" role="waarschuwing">
        {"code": "STOP3101", "ID": "<sch:value-of select="./se:Description/se:Title/normalize-space()"/>", "melding": "De FeatureTypeStyle bevat een Description \"<sch:value-of select="./se:Description/se:Title/normalize-space()"/>\", deze informatie wordt genegeerd.", "ernst": "waarschuwing"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_002" see="se:FeatureTypeName">
      <sch:rule context="se:FeatureTypeName">
         <sch:assert id="STOP3102"
                     test="(string(.) = 'Locatie') or (substring-after(string(.), ':') = 'Locatie')"
                     role="fout">
        {"code": "STOP3102", "ID": "<sch:value-of select="."/>", "melding": "De FeatureTypeStyle:FeatureTypeName is <sch:value-of select="."/>, dit moet Locatie zijn. Wijzig de FeatureTypeName in Locatie (evt. met een namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/).", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_003" see="se:SemanticTypeIdentifier">
      <sch:rule context="se:SemanticTypeIdentifier">
         <sch:let name="AllowedValue"
                  value="'^(geometrie|groepID|kwalitatieveNormwaarde|kwantitatieveNormwaarde)$'"/>
         <sch:assert id="STOP3103"
                     test="matches(substring-after(./string(), ':'), $AllowedValue)"
                     role="fout">
        {"code": "STOP3103", "ID": "<sch:value-of select="."/>", "melding": "De FeatureTypeStyle:SemanticTypeIdentifier is <sch:value-of select="."/>, dit moet geo:geometrie, geo:groepID, geo:kwalitatieveNormwaarde of geo:kwantitatieveNormwaarde zijn (evt. met een andere namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/). Wijzig de SemanticTypeIdentifier.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_004" see="ogc:Filter">
      <sch:rule context="ogc:Filter">
         <sch:let name="SemanticTypeId"
                  value="substring-after(preceding::se:SemanticTypeIdentifier/string(), ':')"/>
         <sch:let name="AllowedValue"
                  value="'^(groepID|kwalitatieveNormwaarde|kwantitatieveNormwaarde)$'"/>
         <sch:assert id="STOP3114"
                     test="matches($SemanticTypeId, $AllowedValue)"
                     role="fout">
        {"code": "STOP3114", "ID": "<sch:value-of select="preceding::se:SemanticTypeIdentifier"/>", "melding": "Rule heeft een Filter terwijl de SemanticTypeIdentifier <sch:value-of select="preceding::se:SemanticTypeIdentifier"/> is. Verwijder het Filter, of wijzig de SemanticTypeIdentifier in geo:groepID, geo:kwalitatieveNormwaarde of geo:kwantitatieveNormwaarde zijn (evt. met een andere namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/).", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_005" see="ogc:PropertyName">
      <sch:rule context="ogc:PropertyName">
         <sch:assert id="STOP3115"
                     test="./string() = substring-after(preceding::se:SemanticTypeIdentifier/string(), ':')"
                     role="fout">
        {"code": "STOP3115", "ID": "<sch:value-of select="."/>", "ID2": "<sch:value-of select="preceding::se:SemanticTypeIdentifier"/>", "melding": "PropertyName is <sch:value-of select="."/>, dit moet overeenkomen met de SemanticTypeIdentifier <sch:value-of select="preceding::se:SemanticTypeIdentifier"/> (zonder namepace prefix). Corrigeer de PropertyName van het filter of pas de SemanticTypeIdentifier aan.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_006" see="ogc:Filter">
      <sch:rule context="ogc:PropertyIsBetween | ogc:PropertyIsNotEqualTo | ogc:PropertyIsLessThan | ogc:PropertyIsGreaterThan | ogc:PropertyIsLessThanOrEqualTo | ogc:PropertyIsGreaterThanOrEqualTo">
         <sch:let name="SemanticTypeId"
                  value="substring-after(preceding::se:SemanticTypeIdentifier/string(), ':')"/>
         <sch:let name="AllowedValue" value="'^(kwantitatieveNormwaarde)$'"/>
         <sch:assert id="STOP3118"
                     test="matches($SemanticTypeId, $AllowedValue)"
                     role="fout">
        {"code": "STOP3118", "ID": "<sch:value-of select="preceding::se:SemanticTypeIdentifier"/>", "melding": "De SemanticTypeIdentifier is <sch:value-of select="preceding::se:SemanticTypeIdentifier"/>. De operator in Rule:Filter is alleen toegestaan bij SemanticTypeIdentifier geo:kwantitatieveNormwaarde (evt. met een andere namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/). Corrigeer de operator of pas de SemanticTypeIdentifier aan.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_007" see="ogc:And">
      <sch:rule context="ogc:And">
         <sch:assert id="STOP3120"
                     test="./ogc:PropertyIsGreaterThanOrEqualTo and ./ogc:PropertyIsLessThan"
                     role="fout">
        {"code": "STOP3120", "ID": "<sch:value-of select="preceding::se:Name"/>", "melding": "In Rule met Rule:Name <sch:value-of select="preceding::se:Name"/> is de operator in Rule:Filter AND, maar de operanden zijn niet PropertyIsLessThan en PropertyIsGreaterThanOrEqualTo. Corrigeer de And expressie in het filter.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_008" see="se:Rule">
      <sch:rule context="se:Rule/se:Description">
         <sch:assert id="STOP3126" test="se:Title/normalize-space() != ''" role="fout">
        {"code": "STOP3126", "ID": "<sch:value-of select="preceding-sibling::se:Name"/>", "melding": "In Rule met Rule:Name <sch:value-of select="preceding-sibling::se:Name"/> is de Description:Title leeg, deze moet een tekst bevatten die in de legenda getoond kan worden. Voeg de legenda tekst toe aan de Description:Title.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_009" see="se:PointSymbolizer">
      <sch:rule context="se:PointSymbolizer">
         <sch:assert id="STOP3135"
                     test="not(./se:Graphic/se:Mark/se:Fill/se:GraphicFill)"
                     role="fout">
        {"code": "STOP3135", "ID": "<sch:value-of select="./se:Name"/>", "melding": "De PointSymbolizer van Rule:Name <sch:value-of select="./se:Name"/> heeft een Mark:Fill:GraphicFill, dit is niet toegestaan. Gebruik SvgParameter.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_010" see="se:SvgParameter">
      <sch:rule context="se:SvgParameter[@name = 'stroke']">
         <sch:assert id="STOP3140"
                     test="matches(./string(), '^#[0-9a-f]{6}$')"
                     role="fout">
       {"code": "STOP3140", "ID": "<sch:value-of select="."/>", "melding": "SvgParameter name=\"stroke\" waarde:<sch:value-of select="."/>, is ongeldig. Vul deze met een valide hexadecimale waarde.", "ernst": "fout"},</sch:assert>
      </sch:rule>
      <sch:rule context="se:SvgParameter[@name = 'fill']">
         <sch:assert id="STOP3147"
                     test="matches(./string(), '^#[0-9a-f]{6}$')"
                     role="fout">
       {"code": "STOP3147", "ID": "<sch:value-of select="."/>", "melding": "SvgParameter name=\"fill\" waarde: <sch:value-of select="."/>, is ongeldig. Vul deze met een valide hexadecimale waarde.", "ernst": "fout"},</sch:assert>
      </sch:rule>
      <sch:rule context="se:SvgParameter[@name = 'stroke-width']">
         <sch:assert id="STOP3141"
                     test="matches(./string(), '^[0-9]+(.[0-9])?[0-9]?$')"
                     role="fout">
       {"code": "STOP3141", "ID": "<sch:value-of select="."/>", "melding": "SvgParameter name=\"stroke-width\" waarde: <sch:value-of select="."/>, is ongeldig. Vul deze met een positief getal met 0,1 of 2 decimalen.", "ernst": "fout"},</sch:assert>
      </sch:rule>
      <sch:rule context="se:SvgParameter[@name = 'stroke-dasharray']">
         <sch:assert id="STOP3142"
                     test="matches(./string(), '^([0-9]+ ?)*$')"
                     role="fout">
       {"code": "STOP3142", "ID": "<sch:value-of select="."/>", "melding": "SvgParameter name=\"stroke-dasharray\" waarde: <sch:value-of select="."/>, is ongeldig. Vul deze met setjes van 2 positief gehele getallen gescheiden door spaties.", "ernst": "fout"},</sch:assert>
      </sch:rule>
      <sch:rule context="se:SvgParameter[@name = 'stroke-linecap']">
         <sch:assert id="STOP3143" test="./string() = 'butt'" role="fout">
       {"code": "STOP3143", "ID": "<sch:value-of select="."/>", "melding": "SvgParameter name=\"stroke-linecap\" waarde: <sch:value-of select="."/>, is ongeldig. Wijzig deze in \"butt\".", "ernst": "fout"},</sch:assert>
      </sch:rule>
      <sch:rule context="se:SvgParameter[@name = 'stroke-opacity']">
         <sch:assert id="STOP3144"
                     test="matches(./string(), '^0((.[0-9])?[0-9]?)|1((.0)?0?)$')"
                     role="fout">
       {"code": "STOP3144", "ID": "<sch:value-of select="."/>", "melding": "SvgParameter name=\"stroke-opacity\" waarde: <sch:value-of select="."/>, is ongeldig. Wijzig deze in een decimaal positief getal tussen 0 en 1 (beide inclusief) met 0,1 of 2 decimalen.", "ernst": "fout"},</sch:assert>
      </sch:rule>
      <sch:rule context="se:SvgParameter[@name = 'fill-opacity']">
         <sch:assert id="STOP3148"
                     test="matches(./string(), '^0((.[0-9])?[0-9]?)|1((.0)?0?)$')"
                     role="fout">
       {"code": "STOP3148", "ID": "<sch:value-of select="."/>", "melding": "SvgParameter name=\"fill-opacity\" waarde: <sch:value-of select="."/>, is ongeldig. Wijzig deze in een decimaal positief getal tussen 0 en 1 (beide inclusief) met 0,1 of 2 decimalen.", "ernst": "fout"},</sch:assert>
      </sch:rule>
      <sch:rule context="se:SvgParameter[@name = 'stroke-linejoin']">
         <sch:assert id="STOP3145" test="./string() = 'round'" role="fout">
       {"code": "STOP3145", "ID": "<sch:value-of select="."/>", "melding": "SvgParameter name=\"stroke-linejoin\" waarde: <sch:value-of select="."/>, is ongeldig. Wijzig deze in \"round\".", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_011" see="se:Stroke/SvgParameter">
      <sch:rule context="se:Stroke/se:SvgParameter">
         <sch:let name="AllowedValue"
                  value="'^(stroke|stroke-width|stroke-dasharray|stroke-linecap|stroke-opacity|stroke-linejoin)$'"/>
         <sch:assert id="STOP3139" test="matches(./@name, $AllowedValue)" role="fout"> 
        {"code": "STOP3139", "ID": "<sch:value-of select="./@name"/>", "melding": "Een Stroke:SvgParameter met een ongeldig name attribute <sch:value-of select="./@name"/>. Maak hier een valide name attribute van.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_012" see="se:Fill/se:SvgParameter">
      <sch:rule context="se:Fill/se:SvgParameter">
         <sch:let name="AllowedValue" value="'^(fill|fill-opacity)$'"/>
         <sch:assert id="STOP3146" test="matches(./@name, $AllowedValue)" role="fout"> 
        {"code": "STOP3146", "ID": "<sch:value-of select="./@name"/>", "melding": "Een Fill:SvgParameter met een ongeldig name attribute <sch:value-of select="./@name"/>. Maak hier een valide name-attribute van.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_013" see="se:WellKnownName">
      <sch:rule context="se:WellKnownName">
         <sch:let name="AllowedValue"
                  value="'^(cross|cross_fill|square|circle|star|triangle)$'"/>
         <sch:assert id="STOP3157" test="matches(./string(), $AllowedValue)" role="fout">
        {"code": "STOP3157", "ID": "<sch:value-of select="."/>", "melding": "De Mark:WellKnownName <sch:value-of select="."/> is niet toegestaan. Maak hier cross(of cross_fill), square, circle, star of triangle van.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_014" see="se:Size">
      <sch:rule context="se:Size">
         <sch:assert id="STOP3163" test="matches(./string(), '^[0-9]+$')" role="fout">
       {"code": "STOP3163", "ID": "<sch:value-of select="../../se:Name"/>", "ID2": "<sch:value-of select="."/>", "melding": "De (Point/Polygon)symbolizer met se:Name <sch:value-of select="../../se:Name"/> heeft een ongeldige Graphic:Size <sch:value-of select="."/>. Wijzig deze in een geheel positief getal.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_016"
                see="se:PolygonSymbolizer/se:Fill/se:GraphicFill/se:Graphic">
      <sch:rule context="se:PolygonSymbolizer/se:Fill/se:GraphicFill/se:Graphic">
         <sch:assert id="STOP3170"
                     test="./se:ExternalGraphic and not(./se:Mark)"
                     role="fout">
        {"code": "STOP3170", "ID": "<sch:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>", "melding": "De PolygonSymbolizer:Fill:GraphicFill:Graphic met Name <sch:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/> bevat geen se:ExternalGraphic of ook een se:Mark, dit is wel vereist. Voeg een se:ExternalGraphic element toe.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_017" see="se:InlineContent[@encoding='base64']">
      <sch:rule context="se:InlineContent[@encoding = 'base64']">
         <sch:assert id="STOP3173"
                     test="matches(./normalize-space(), '^[A-Z0-9a-z+/ =]*$')"
                     role="fout">
       {"code": "STOP3173", "ID": "<sch:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>", "ID2": "<sch:value-of select="normalize-space(replace(./string(), '[A-Z0-9a-z+/ =]', ''))"/>", "melding": "De PolygonSymbolizer:Fill:GraphicFill:Graphic:ExternalGraphic:InlineContent van Rule:Name <sch:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/> bevat ongeldige tekens <sch:value-of select="normalize-space(replace(./string(), '[A-Z0-9a-z+/ =]', ''))"/>. Wijzig dit. Een base64 encodig mag alleen bestaan uit: hoofd- en kleine letters, cijfers, spaties, plus-teken, /-teken en =-teken.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_018" see="se:ExternalGraphic/se:Format">
      <sch:rule context="se:ExternalGraphic/se:Format">
         <sch:assert id="STOP3174" test="./string() = 'image/png'" role="fout">
       {"code": "STOP3174", "ID": "<sch:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/>", "ID2": "<sch:value-of select="."/>", "melding": "De ExternalGraphic:Format van (Polygon)symbolizer:Name <sch:value-of select="ancestor::se:PolygonSymbolizer/se:Name"/> heeft een ongeldig Format <sch:value-of select="."/>. Wijzig deze in image/png", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_3176" see="se:FeatureTypeStyle">
      <sch:rule context="se:FeatureTypeStyle">
         <sch:let name="childnames">
            <xsl:for-each select="child::*">
               <xsl:value-of select="node-name(.)"/>
               <xsl:if test="count(following-sibling::*) &gt; 0">, </xsl:if>
            </xsl:for-each>
         </sch:let>
         <sch:assert id="STOP3176"
                     test="count(child::*) = 0 or (se:FeatureTypeName and se:SemanticTypeIdentifier and se:Rule)"
                     role="fout">
       {"code": "STOP3176", "childnames": "<sch:value-of select="$childnames"/>", "melding": "FeatureTypeStyle heeft child-elementen: <sch:value-of select="$childnames"/>. Dit is niet correct. FeatureTypeStyle moet FeatureTypeName èn SemanticTypeIdentifier èn een of meer Rule's bevatten OF leeg zijn. Maak de FeatureTypeStyle compleet of verwijder alle child-elementen binnen FeatureTypeStyle.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_3177" see="se:PointSymbolizer">
      <sch:rule context="se:PointSymbolizer">
         <sch:assert id="STOP3177"
                     test="not(./se:Graphic/se:ExternalGraphic)"
                     role="fout">
        {"code": "STOP3177", "ID": "<sch:value-of select="./se:Name"/>", "melding": "De PointSymbolizer:Name <sch:value-of select="./se:Name"/> bevat het element se:ExternalGraphic, dit is niet toegestaan. Pas de PointSymbolizer aan, gebruik se:PointSymbolizer/se:Graphic/se:Mark/se:WellKnownName.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_3178" see="se:PointSymbolizer">
      <sch:rule context="se:PointSymbolizer">
         <sch:assert id="STOP3178" test="./se:Graphic/se:Mark/se:Fill" role="fout">
        {"code": "STOP3178", "ID": "<sch:value-of select="./se:Name"/>", "melding": "De PointSymbolizer:Name <sch:value-of select="./se:Name"/> bevat geen se:Fill, dit is niet toegestaan. Pas de PointSymbolizer aan.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_3179" see="se:PointSymbolizer">
      <sch:rule context="se:PointSymbolizer">
         <sch:assert id="STOP3179" test="./se:Graphic/se:Mark/se:Stroke" role="fout">
        {"code": "STOP3179", "ID": "<sch:value-of select="./se:Name"/>", "melding": "De PointSymbolizer:Name <sch:value-of select="./se:Name"/> bevat geen se:Stroke, dit is niet toegestaan. Pas de PointSymbolizer aan.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_3180" see="se:Rule">
      <sch:rule context="se:Rule">
         <sch:let name="SemanticTypeId"
                  value="substring-after(preceding::se:SemanticTypeIdentifier/string(), ':')"/>
         <sch:let name="AllowedValue"
                  value="'^(groepID|kwalitatieveNormwaarde|kwantitatieveNormwaarde)$'"/>
         <sch:report id="STOP3180"
                     test="matches($SemanticTypeId, $AllowedValue) and not(./ogc:Filter)"
                     role="fout"> 
        {"code": "STOP3180", "ID": "<sch:value-of select="preceding::se:SemanticTypeIdentifier"/>", "ID2": "<sch:value-of select="./se:Name"/>", "melding": "Rule <sch:value-of select="./se:Name"/> heeft geen Filter terwijl de SemanticTypeIdentifier <sch:value-of select="preceding::se:SemanticTypeIdentifier"/> is. Voeg een Filter toe of wijzig de SemanticTypeIdentifier in geo:geometrie (evt. met een andere namespace prefix voor https://standaarden.overheid.nl/stop/imop/geo/).", "ernst": "fout"},</sch:report>
      </sch:rule>
   </sch:pattern>
   <sch:pattern id="sch_se_3181" see="se:PolygonSymbolizer">
      <sch:rule context="se:PolygonSymbolizer">
         <sch:assert id="STOP3181" test="se:Stroke or se:Fill" role="fout">
        {"code": "STOP3181", "ID": "<sch:value-of select="se:Name"/>", "melding": "PolygonSymbolizer <sch:value-of select="se:Name"/> heeft geen Fill of Stroke. Voeg een Fill en/of Stroke toe.", "ernst": "fout"},</sch:assert>
      </sch:rule>
   </sch:pattern>
</sch:schema>
