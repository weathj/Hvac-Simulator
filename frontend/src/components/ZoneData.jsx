import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { useZones } from '../hooks/useZones'
import { Panel, StatRow, SliderRow } from './PanelComponents'
import './PanelComponents.css'
import './ZoneData.css'

function buildChartData(trend_logs) {
    const temps = trend_logs?.zone_temp ?? {}
    const spts  = trend_logs?.zone_spt  ?? {}
    return Object.keys(temps).map(tick => ({
        t:        tick,
        air_temp: temps[tick],
        setpoint: spts[tick],
    }))
}

function ZoneCard({ zone }) {
    const chartData = buildChartData(zone.trend_logs)
    return (
        <div className="zone-grid">
            <Panel title={zone.name} variant="zone">
                <StatRow label="Temperature"           value={zone.air_temp}   unit=" °F" decimals={2} />
                <StatRow label="Setpoint"              value={zone.setpoint}   unit=" °F" />
                <StatRow label="Supply Air Temperature" value={zone.vav_sa_temp} unit=" °F" decimals={2} />
                <SliderRow label="VAV Damper Position" zone_id={zone.id} point_name="vav_dpr_pos" value={zone.vav_dpr_pos} unit=" %" min={0} max={100} />
                <div className="zone-chart-area">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={chartData}>
                            <XAxis dataKey="t"  stroke="#3b434d" tick={{ fontSize: 10, fill: '#636e7b' }} />
                            <YAxis              stroke="#3b434d" tick={{ fontSize: 10, fill: '#636e7b' }} domain={['auto', 'auto']} />
                            <Tooltip contentStyle={{ background: '#0d1117', border: '1px solid #21262d', fontSize: '0.7rem' }} />
                            <Line type="monotone" dataKey="air_temp" stroke="#1d00d9" dot={false} strokeWidth={1.5} />
                            <Line type="monotone" dataKey="setpoint" stroke="#bf0303" dot={false} strokeWidth={1.5} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </Panel>
        </div>
    )
}

export default function ZoneData() {
    const { data, error } = useZones()

    if (error) return <div className="fault-banner">&#x26a0; FAULT &mdash; {error}</div>
    if (!data || data.length === 0) return <div className="zone-empty">No zones configured</div>

    return (
        <div className="zone-grid">
            {data.map(zone => (
                <ZoneCard key={zone.id} zone={zone} />
            ))}
        </div>
    )
}
