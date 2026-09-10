<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" esdlVersion="v2401" id="f92a4dc7-e4b3-4799-851e-bc689e6d1316" version="23" description="" name="Untitled EnergySystem">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="06f78cd5-f48f-48a9-bed0-4e49e6b733ce">
    <carriers xsi:type="esdl:Carriers" id="7f6bcb28-b5a7-4596-839f-9f311cb3e6e2">
      <carrier xsi:type="esdl:ElectricityCommodity" name="Electricity" id="7b4fae51-49a6-439c-9517-1932af396c04"/>
      <carrier xsi:type="esdl:GasCommodity" name="Hydrogen" id="f5ee1b63-9a7a-480f-bdae-2215df27a87a"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="0922dfcb-d096-48a4-9354-8f4c4551939b" name="Untitled Instance">
    <area xsi:type="esdl:Area" id="8b038f6c-9db3-48bf-8566-c4bb02200514" name="Untitled Area">
      <asset xsi:type="esdl:WindPark" surfaceArea="196936609" name="TNVDW" commissioningDate="2028-01-01T09:00:00.285000+0100" power="700000000.0" id="4d8cdd59-735f-4ac4-bb55-095e5864a199" decommissioningDate="2056-01-01T09:00:00.693000+0100">
        <port xsi:type="esdl:OutPort" id="59cf5288-da4f-4ae3-97b3-c22a6a6e698b" connectedTo="d497cef9-2c0e-4c41-8aa5-649147583eca" name="Out"/>
        <geometry xsi:type="esdl:Polygon" CRS="WGS84">
          <exterior xsi:type="esdl:SubPolygon">
            <point xsi:type="esdl:Point" lon="5.865325927734376" lat="54.00524035227916"/>
            <point xsi:type="esdl:Point" lon="5.805244445800781" lat="54.05481834478634"/>
            <point xsi:type="esdl:Point" lon="4.762573242187501" lat="54.01452933495446"/>
          </exterior>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" name="NewCostInformation" id="892a63fd-0653-434c-8eac-17c6623c3f24">
          <discountRate xsi:type="esdl:SingleValue" value="7.75" id="eab59490-6421-42e6-87f1-ff2dea272113" name="NewSingleValue">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="8c14ac28-fa3f-4264-96ed-59d63db711a7" unit="PERCENT" physicalQuantity="COST"/>
          </discountRate>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="1.5" name="NewSingleValue" id="02df7a04-9816-4bf2-aac5-ad38175ccb0a">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="62af67de-162b-4c82-bb7a-72518a35fbc7" unit="PERCENT" physicalQuantity="COST"/>
          </fixedOperationalAndMaintenanceCosts>
          <investmentCosts xsi:type="esdl:SingleValue" value="1225.0" name="NewSingleValue" id="c49faf9f-6607-4301-a090-55facd85f9c3">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="700ab724-69cf-4219-9616-2f0dad3baa6e" multiplier="MEGA" unit="EURO" physicalQuantity="COST"/>
          </investmentCosts>
          <variableOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="4.0" name="NewSingleValue" id="006397e3-4183-4427-8d89-155900a3dd3f">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="WATTHOUR" id="7c46126e-1e63-42a2-8bfa-82242ed5279f" unit="EURO" physicalQuantity="COST" perMultiplier="MEGA"/>
          </variableOperationalAndMaintenanceCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:Electrolyzer" power="500.0" efficiency="0.6" name="Electrolyzer" commissioningDate="2031-01-01T09:00:00.598000+0100" id="e5965f75-8d64-4c3b-ad3a-3a3ce8bc80ed" decommissioningDate="2056-01-01T09:00:00.703000+0100">
        <port xsi:type="esdl:InPort" id="a0184716-0793-4531-b14b-417b69f41c81" name="In" connectedTo="a91027c3-e6c7-4922-bcf1-f52bfa394c8d"/>
        <port xsi:type="esdl:OutPort" name="Out" carrier="f5ee1b63-9a7a-480f-bdae-2215df27a87a" connectedTo="d188e8b6-6ae4-4897-8a16-5b17a0a55513" id="f7b6fc6e-3adb-4630-aacc-342497f0da88"/>
        <geometry xsi:type="esdl:Point" lon="5.856399536132813" lat="54.03118512267593" CRS="WGS84"/>
        <costInformation xsi:type="esdl:CostInformation" name="NewCostInformation" id="2f8557a8-c3c6-4495-891b-b9e1c5679d08">
          <discountRate xsi:type="esdl:SingleValue" value="7.0" id="513f625f-ee01-4fec-b891-de442b8de76b" name="NewSingleValue">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="2ce69645-74f4-41d9-ba1b-e57b2fb6bd2f" unit="PERCENT" physicalQuantity="COST"/>
          </discountRate>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" value="2.0" name="NewSingleValue" id="e889996b-672e-4efc-ad75-fa720911f624">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="046afe60-b36f-4377-8036-1a101717bae7" unit="PERCENT" physicalQuantity="COST"/>
          </fixedOperationalAndMaintenanceCosts>
          <investmentCosts xsi:type="esdl:SingleValue" value="1050.0" name="NewSingleValue" id="415a8639-d736-48a8-a01e-19b350c57642">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="81f6a5f4-7f5b-49e1-a736-0aeecc098d53" multiplier="MEGA" unit="EURO" physicalQuantity="COST"/>
          </investmentCosts>
          <variableOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" name="NewSingleValue" id="65682f7d-edb4-4aee-943e-deff4325f2a9">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="WATTHOUR" id="f7289b8b-5acd-442a-b194-6c2504f0674d" unit="EURO" physicalQuantity="COST" perMultiplier="MEGA"/>
          </variableOperationalAndMaintenanceCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:GasDemand" name="Offtaker" power="24900000.0" id="4fdd2fda-9d60-4d82-821a-bbadd6720a36" operationalHours="8760">
        <port xsi:type="esdl:InPort" name="In" carrier="f5ee1b63-9a7a-480f-bdae-2215df27a87a" connectedTo="788355b0-1ea9-4d5e-bc98-0792f2fc3f59" id="8d787533-3663-4dc7-b339-681ad3724065"/>
        <geometry xsi:type="esdl:Point" lon="6.972241401672364" lat="53.315420710904455" CRS="WGS84"/>
        <costInformation xsi:type="esdl:CostInformation" name="NewCostInformation" id="3e58aaa9-f17c-4393-be1d-123bbbc54f6f">
          <discountRate xsi:type="esdl:SingleValue" value="9.5" id="7b324fda-fcd3-466e-87c7-a498cf075726" name="NewSingleValue">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="44c94e03-0b9d-4d65-bcd3-ee9fb9549b61" unit="PERCENT" physicalQuantity="COST"/>
          </discountRate>
          <fixedOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" name="NewSingleValue" id="cb0a8dc9-577d-4874-b0ce-29b2d2f4c137">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="6abbc85b-b93d-4f46-87b7-305303a04ca2" unit="EURO" physicalQuantity="COST"/>
          </fixedOperationalAndMaintenanceCosts>
          <investmentCosts xsi:type="esdl:SingleValue" name="NewSingleValue" id="2be66c99-077c-4b2c-b62f-99fbde5be9c5">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="a4fbc0b0-5482-432a-b3f1-8833ae118285" unit="EURO" physicalQuantity="COST"/>
          </investmentCosts>
          <variableOperationalAndMaintenanceCosts xsi:type="esdl:SingleValue" name="NewSingleValue" id="45fba061-a9b9-4473-8097-21159a5bfe3f">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" id="3ca01762-758f-43ba-8686-ff6085c79d84" unit="EURO" physicalQuantity="COST"/>
          </variableOperationalAndMaintenanceCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:ElectricityCable" name="ElectricityCable" length="24743.7" id="61ae9a5c-c5d8-47a0-a7da-a54432d38fc9">
        <port xsi:type="esdl:InPort" id="d497cef9-2c0e-4c41-8aa5-649147583eca" name="In" connectedTo="59cf5288-da4f-4ae3-97b3-c22a6a6e698b"/>
        <port xsi:type="esdl:OutPort" id="a91027c3-e6c7-4922-bcf1-f52bfa394c8d" connectedTo="a0184716-0793-4531-b14b-417b69f41c81" name="Out"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lon="5.477714538574219" lat="54.02486267733999"/>
          <point xsi:type="esdl:Point" lon="5.856399536132813" lat="54.03118512267593"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Pipe" length="108334.3" name="H2-pipe" id="2a891589-2856-4365-90da-bd3d7d8d1d3b">
        <port xsi:type="esdl:InPort" name="In" carrier="f5ee1b63-9a7a-480f-bdae-2215df27a87a" connectedTo="f7b6fc6e-3adb-4630-aacc-342497f0da88" id="d188e8b6-6ae4-4897-8a16-5b17a0a55513"/>
        <port xsi:type="esdl:OutPort" name="Out" carrier="f5ee1b63-9a7a-480f-bdae-2215df27a87a" connectedTo="8d787533-3663-4dc7-b339-681ad3724065" id="788355b0-1ea9-4d5e-bc98-0792f2fc3f59"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lon="5.856399536132813" lat="54.03118512267593"/>
          <point xsi:type="esdl:Point" lon="6.972241401672364" lat="53.315420710904455"/>
        </geometry>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
