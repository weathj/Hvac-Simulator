import { useState } from 'react'
import { Panel, StatRow } from './PanelComponents'
import { useAHU } from '../hooks/useAHU'
import AirUnitData from './AirUnitData'
import ZoneData from './ZoneData'
import './Dashboard.css'
import './PanelComponents.css'

function IconZones() {
    return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
            <rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>
        </svg>
    )
}

function IconAHU() {
    return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
        </svg>
    )
}

function IconOutdoor() {
    return (
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="5"/>
            <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
        </svg>
    )
}

export default function Dashboard() {
    const [mobilePage, setMobilePage] = useState('zones')
    const { data, error } = useAHU()
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
                <div className={`shell-sidebar${mobilePage === 'outdoor' ? ' mobile-active' : ''}`}>
                    <Panel title="Location" variant="outside">
                        <StatRow label="Temperature" value={ahu?.oa_temp}      unit=" °F" decimals={2} />
                        <StatRow label="Humidity"    value={ahu?.oa_humidity}  unit=" %"               />
                    </Panel>
                </div>

                <main className={`shell-content${mobilePage !== 'zones' ? ' mobile-hidden' : ''}`}>
                    <ZoneData />
                </main>

                <div className={`shell-info${mobilePage === 'ahu' ? ' mobile-active' : ''}`}>
                    <AirUnitData />
                </div>
            </div>

            <nav className="mobile-nav">
                <button className={mobilePage === 'zones'   ? 'active' : ''} onClick={() => setMobilePage('zones')}>
                    <IconZones /> Zones
                </button>
                <button className={mobilePage === 'ahu'     ? 'active' : ''} onClick={() => setMobilePage('ahu')}>
                    <IconAHU /> AHU
                </button>
                <button className={mobilePage === 'outdoor' ? 'active' : ''} onClick={() => setMobilePage('outdoor')}>
                    <IconOutdoor /> Outdoor
                </button>
            </nav>

        </div>
    )
}
