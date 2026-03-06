import { Panel, StatRow, AdjustRow, SliderRow } from './PanelComponents'
import { useAHU } from '../hooks/useAHU'
import './PanelComponents.css'

export default function AirUnitData() {
    const { data, error } = useAHU()
    const ahu = data?.[0]

    if (error) return <div className="fault-banner">&#x26a0; FAULT &mdash; {error}</div>

    return (
        <div className="panel-grid">
                <Panel title="Supply Air" variant="supply">
                    <StatRow label="Temperature"  value={ahu?.sa_temp}           unit=" °F"     decimals={2} />
                    <StatRow label="Humidity"     value={ahu?.sa_humidity}       unit=" %"                   />
                    <StatRow label="BTU"          value={ahu?.sa_btu}            unit=" BTU/hr" decimals={2} />
                    <StatRow label="Flow"         value={ahu?.sa_flow}           unit=" CFM"                 />
                    <SliderRow label="Fan Speed" point_name="sa_fan_speed"    value={ahu?.sa_fan_speed}      unit=" %"                   />
                    <AdjustRow label="Cooling Coil" point_name="cooling_coil_temp" locked_point="heating_coil_temp" value={ahu?.cooling_coil_temp} unit=" °F" decimals={2} max={70} />
                    <AdjustRow label="Heating Coil" point_name="heating_coil_temp" locked_point="cooling_coil_temp" value={ahu?.heating_coil_temp} unit=" °F" decimals={2} min={65} />
                </Panel>

                <Panel title="Mixed Air" variant="mixed">
                    <StatRow label="Temperature"     value={ahu?.ma_temp}             unit=" °F"     decimals={2} />
                    <StatRow label="Humidity"        value={ahu?.ma_humidity}         unit=" %"                   />
                    <StatRow label="BTU"             value={ahu?.ma_btu}              unit=" BTU/hr" decimals={2} />
                    <StatRow label="Flow"            value={ahu?.ma_flow}             unit=" CFM"                     />
                    <SliderRow label="Damper Position" point_name="ma_damper_position" value={ahu?.ma_damper_position}  unit="%"                    />
                </Panel>

                <Panel title="Return Air" variant="return">
                    <StatRow label="Temperature" value={ahu?.ra_temp} unit=" °F"  decimals={2} />
                    <StatRow label="Flow"        value={ahu?.ra_flow} unit=" CFM"              />
                    <SliderRow label="Fan Speed"   point_name="ra_fan_speed" value={ahu?.ra_fan_speed} unit=" %"           />
                </Panel>
                
                <Panel title="Exhaust Air" variant="exhaust">
                    <SliderRow label="Damper Position" point_name="ea_damper_position" value={ahu?.ea_damper_position} unit="%" />
                </Panel>
                <Panel title="Outside Air" variant="outside">
                    <AdjustRow label="Temperature"   point_name="oa_temp" value={ahu?.oa_temp}           unit=" °F"     decimals={2} />
                    <StatRow label="Humidity"        value={ahu?.oa_humidity}       unit=" %"                   />
                    <StatRow label="BTU"             value={ahu?.oa_btu}            unit=" BTU/hr" decimals={2} />
                    <StatRow label="Outdoor Flow"    value={ahu?.outdoor_air_flow}  unit=" CFM"    decimals={2} />
                    <SliderRow label="Damper Position" point_name="oa_damper_position" value={ahu?.oa_damper_position} unit="%"                   />
                </Panel>
            </div>
    )
}
