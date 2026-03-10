import { useState } from 'react'
import { Panel, StatRow, AdjustRow, SliderRow } from './PanelComponents'
import { useAHU } from '../hooks/useAHU'
import AirUnitData from './AirUnitData'
import ZoneData from './ZoneData'
import './Dashboard.css'
import './PanelComponents.css'

export default function Dashboard() {
    const [page, setPage] = useState('data')
    const { data, error } = useAHU()
    const { PostData } = useAHU()
    const ahu = data?.[0]

    if (error) return <div className="fault-banner">&#x26a0; FAULT &mdash; {error}</div>

    return (
        <div className="shell">

            <header className="shell-header">
                <div className="shell-header-left">
                    <span className="shell-system-id">AHU-01</span>
                    <span className="shell-system-name">Building Automation System</span>
                </div>
                <div className="shell-header-right">
                    <span className="shell-version">HVAC Simulator v1.0</span>
                </div>
            </header>

            <div className="shell-body">
                <div className="shell-sidebar">
                    <Panel title="Location" variant="outside">
                        <StatRow label="Temperature"     value={ahu?.oa_temp}           unit=" °F"     decimals={2} />
                        <StatRow label="Humidity"        value={ahu?.oa_humidity}       unit=" %"                   />
                    </Panel>
                </div>

                <main className="shell-content">
                    <ZoneData />
                </main>

                <div className="shell-info">
                    {page === 'data' && <AirUnitData />}
                </div>

            </div>
        </div>
    )
}
