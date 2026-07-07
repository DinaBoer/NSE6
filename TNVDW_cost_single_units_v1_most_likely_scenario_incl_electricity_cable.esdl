<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="Untitled EnergySystem" esdlVersion="v2401" description="" id="f92a4dc7-e4b3-4799-851e-bc689e6d1316" version="22">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="06f78cd5-f48f-48a9-bed0-4e49e6b733ce">
    <carriers xsi:type="esdl:Carriers" id="7f6bcb28-b5a7-4596-839f-9f311cb3e6e2">
      <carrier xsi:type="esdl:ElectricityCommodity" id="7b4fae51-49a6-439c-9517-1932af396c04" name="Electricity"/>
      <carrier xsi:type="esdl:GasCommodity" id="f5ee1b63-9a7a-480f-bdae-2215df27a87a" name="Hydrogen"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="0922dfcb-d096-48a4-9354-8f4c4551939b" name="Untitled Instance">
    <area xsi:type="esdl:Area" name="Untitled Area" id="8b038f6c-9db3-48bf-8566-c4bb02200514">
      <asset xsi:type="esdl:WindPark" name="TNVDW" decommissioningDate="2056-01-01T09:00:00.693000+0100" power="700000000.0" commissioningDate="2028-01-01T09:00:00.285000+0100" id="4d8cdd59-735f-4ac4-bb55-095e5864a199" surfaceArea="196936609">
        <port xsi:type="esdl:OutPort" name="Out" id="59cf5288-da4f-4ae3-97b3-c22a6a6e698b" connectedTo="d497cef9-2c0e-4c41-8aa5-649147583eca 04f2e994-2870-4177-a4cc-b781e4419404"/>
        <geometry xsi:type="esdl:Polygon" CRS="WGS84">
          <exterior xsi:type="esdl:SubPolygon">
            <point xsi:type="esdl:Point" lon="5.865325927734376" lat="54.00524035227916"/>
            <point xsi:type="esdl:Point" lon="5.805244445800781" lat="54.05481834478634"/>
            <point xsi:type="esdl:Point" lon="4.762573242187501" lat="54.01452933495446"/>
          </exterior>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" name="NewCostInformation" id="892a63fd-0653-434c-8eac-17c6623c3f24">
          <discountRate xsi:type="esdl:SingleValue" id="b18d8748-7177-4225-8b73-f1a24b842c77" value="8.5" name="NewSingleValue">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="748a53e5-1962-4e71-8f6e-5647d2849284" physicalQuantity="COST" unit="PERCENT"/>
          </discountRate>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="2.25" name="NewSingleValue" id="02df7a04-9816-4bf2-aac5-ad38175ccb0a">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="62af67de-162b-4c82-bb7a-72518a35fbc7" physicalQuantity="COST" unit="PERCENT"/>
          </fixedOperationalAndMaintenanceCosts>
          <investmentCosts xsi:type="esdl:SingleValue" value="1750.0" name="NewSingleValue" id="c49faf9f-6607-4301-a090-55facd85f9c3">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="700ab724-69cf-4219-9616-2f0dad3baa6e" multiplier="MEGA" physicalQuantity="COST" unit="EURO"/>
          </investmentCosts>
          <variableOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="5.0" name="NewSingleValue" id="006397e3-4183-4427-8d89-155900a3dd3f">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perMultiplier="MEGA" physicalQuantity="COST" unit="EURO" id="7c46126e-1e63-42a2-8bfa-82242ed5279f" perUnit="WATTHOUR"/>
          </variableOperationalAndMaintenanceCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:Electrolyzer" name="Electrolyzer" decommissioningDate="2056-01-01T09:00:00.703000+0100" commissioningDate="2031-01-01T09:00:00.598000+0100" id="e5965f75-8d64-4c3b-ad3a-3a3ce8bc80ed" efficiency="0.6" power="500.0">
        <port xsi:type="esdl:InPort" name="In" id="a0184716-0793-4531-b14b-417b69f41c81" connectedTo="a91027c3-e6c7-4922-bcf1-f52bfa394c8d"/>
        <port xsi:type="esdl:OutPort" carrier="f5ee1b63-9a7a-480f-bdae-2215df27a87a" name="Out" id="f7b6fc6e-3adb-4630-aacc-342497f0da88" connectedTo="d188e8b6-6ae4-4897-8a16-5b17a0a55513"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="5.856399536132813" lat="54.03118512267593"/>
        <costInformation xsi:type="esdl:CostInformation" name="NewCostInformation" id="2f8557a8-c3c6-4495-891b-b9e1c5679d08">
          <discountRate xsi:type="esdl:SingleValue" id="79461c01-8dcb-4851-905a-6ca40171820b" value="8.25" name="NewSingleValue">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="d1bbd143-18a5-4f95-9573-9bc11cc1287b" physicalQuantity="COST" unit="PERCENT"/>
          </discountRate>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="2.0" name="NewSingleValue" id="e889996b-672e-4efc-ad75-fa720911f624">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="046afe60-b36f-4377-8036-1a101717bae7" physicalQuantity="COST" unit="PERCENT"/>
          </fixedOperationalAndMaintenanceCosts>
          <investmentCosts xsi:type="esdl:SingleValue" value="2000.0" name="NewSingleValue" id="415a8639-d736-48a8-a01e-19b350c57642">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="81f6a5f4-7f5b-49e1-a736-0aeecc098d53" multiplier="MEGA" physicalQuantity="COST" unit="EURO"/>
          </investmentCosts>
          <variableOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" name="NewSingleValue" id="65682f7d-edb4-4aee-943e-deff4325f2a9">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perMultiplier="MEGA" physicalQuantity="COST" unit="EURO" id="f7289b8b-5acd-442a-b194-6c2504f0674d" perUnit="WATTHOUR"/>
          </variableOperationalAndMaintenanceCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:GasDemand" operationalHours="8760" name="Offtaker" power="24900000.0" id="4fdd2fda-9d60-4d82-821a-bbadd6720a36">
        <port xsi:type="esdl:InPort" carrier="f5ee1b63-9a7a-480f-bdae-2215df27a87a" name="In" id="8d787533-3663-4dc7-b339-681ad3724065" connectedTo="788355b0-1ea9-4d5e-bc98-0792f2fc3f59"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="6.972241401672364" lat="53.315420710904455"/>
        <costInformation xsi:type="esdl:CostInformation" name="NewCostInformation" id="95874973-a041-4bd6-b795-7134b69684e5">
          <discountRate xsi:type="esdl:SingleValue" value="10.5" name="NewSingleValue" id="7f37ae56-b9b1-4c09-8e9c-b7a3a304582f">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="6b645073-c3ef-4c6e-a196-d268bb5a8854" physicalQuantity="COST" unit="PERCENT"/>
          </discountRate>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" id="bae0168f-2205-4a64-a422-5b3984400681" name="NewSingleValue">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="227e0144-1d30-4d21-abd2-d7037e9db424" physicalQuantity="COST" unit="EURO"/>
          </fixedOperationalAndMaintenanceCosts>
          <investmentCosts xsi:type="esdl:SingleValue" id="2aea002e-3f35-4960-b057-43bd5cdd4059" name="NewSingleValue">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="d01d4924-8f03-4fea-9261-311048d54e64" physicalQuantity="COST" unit="EURO"/>
          </investmentCosts>
          <variableOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" id="696ab6cc-5711-4337-8a91-7cd9bbbdadc6" name="NewSingleValue">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="8883eea0-4d49-4a36-9d35-9d63a21f551c" physicalQuantity="COST" unit="EURO"/>
          </variableOperationalAndMaintenanceCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:ElectricityCable" name="ElectricityCable OWF to EL" length="24743.7" id="61ae9a5c-c5d8-47a0-a7da-a54432d38fc9">
        <port xsi:type="esdl:InPort" name="In" id="d497cef9-2c0e-4c41-8aa5-649147583eca" connectedTo="59cf5288-da4f-4ae3-97b3-c22a6a6e698b"/>
        <port xsi:type="esdl:OutPort" name="Out" id="a91027c3-e6c7-4922-bcf1-f52bfa394c8d" connectedTo="a0184716-0793-4531-b14b-417b69f41c81"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lon="5.477714538574219" lat="54.02486267733999"/>
          <point xsi:type="esdl:Point" lon="5.856399536132813" lat="54.03118512267593"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" length="108334.3" name="H2-pipe" id="2a891589-2856-4365-90da-bd3d7d8d1d3b">
        <port xsi:type="esdl:InPort" carrier="f5ee1b63-9a7a-480f-bdae-2215df27a87a" name="In" id="d188e8b6-6ae4-4897-8a16-5b17a0a55513" connectedTo="f7b6fc6e-3adb-4630-aacc-342497f0da88"/>
        <port xsi:type="esdl:OutPort" carrier="f5ee1b63-9a7a-480f-bdae-2215df27a87a" name="Out" id="788355b0-1ea9-4d5e-bc98-0792f2fc3f59" connectedTo="8d787533-3663-4dc7-b339-681ad3724065"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lon="5.856399536132813" lat="54.03118512267593"/>
          <point xsi:type="esdl:Point" lon="6.972241401672364" lat="53.315420710904455"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:ElectricityDemand" name="ElectricityDemand_2557" id="25570af5-268c-4e3d-a8b3-9db829872ba3">
        <port xsi:type="esdl:InPort" name="In" id="04dfee30-2fda-409a-9e6f-d08ffaa4e17b" connectedTo="ed891413-59ba-4f4f-8804-935b90e9c07b"/>
        <geometry xsi:type="esdl:Point" CRS="WGS84" lon="6.863846217798791" lat="53.443696501774525"/>
      </asset>
      <asset xsi:type="esdl:ElectricityCable" name="ElectricityCable OWF to Eemshaven" length="111749.3" id="8c45f0ef-7ef4-4140-a5a4-1f1e58081426">
        <port xsi:type="esdl:InPort" name="In" id="04f2e994-2870-4177-a4cc-b781e4419404" connectedTo="59cf5288-da4f-4ae3-97b3-c22a6a6e698b"/>
        <port xsi:type="esdl:OutPort" name="Out" id="ed891413-59ba-4f4f-8804-935b90e9c07b" connectedTo="04dfee30-2fda-409a-9e6f-d08ffaa4e17b"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lon="5.477714538574219" lat="54.02486267733999"/>
          <point xsi:type="esdl:Point" lon="6.863846217798791" lat="53.443696501774525"/>
        </geometry>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
