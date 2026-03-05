import { useState } from 'react'
import AirUnitData from './AirUnitData'
import ZoneData from './ZoneData'
import './Dashboard.css'
import './PanelComponents.css'

function LocationCard() {
    return (
        <div className="panel">
            <div className="panel-header panel-header--outside">
                <div className="panel-dot" />
                <span className="panel-title">Location</span>
            </div>
            <div className="panel-body">
                <div className="stat-row">
                    <span className="stat-label">Temperature</span>
                    <span className="stat-value">80.0 °F</span>
                </div>
                <div className="stat-row">
                    <span className="stat-label">Humidity</span>
                    <span className="stat-value">40.0 % Rh</span>
                </div>
            </div>
        </div>
    )
}

export default function Dashboard() {
    const [page, setPage] = useState('data')

    return (
        <div className="shell">

            <header className="shell-header">
                <div className="shell-header-left">
                    <span className="shell-system-id">AHU-01</span>
                    <span className="shell-system-name">Building Automation System</span>
                </div>
                <div className="shell-header-right">
                    <span className="shell-version">HVAC Simulator v0.1</span>
                </div>
            </header>

            <div className="shell-body">
                <div className="shell-sidebar">
                    <LocationCard />
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
