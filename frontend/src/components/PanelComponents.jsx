import { useState, useEffect } from 'react'
import { useZones } from "../hooks/useZones"
import { Slider } from "@mui/material"

export function Panel({ title, variant, children }) {
    return (
        <div className="panel">
            <div className={`panel-header panel-header--${variant}`}>
                <div className="panel-dot" />
                <span className="panel-title">{title}</span>
            </div>
            <div className="panel-body">
                {children}
            </div>
        </div>
    )
}

export function StatRow({ label, value, unit, decimals, onClick }) {
    const formatted = value !== undefined && value !== null
        ? (decimals !== undefined ? Number(value).toFixed(decimals) : value)
        : null
    const display = formatted != null ? `${formatted}${unit}` : '—'
    return (
        <div className="stat-row" onClick={onClick} style={onClick ? { cursor: 'pointer' } : undefined}>
            <span className="stat-label">{label}</span>
            <span className="stat-value">{display}</span>
        </div>
    )
}

export function SliderRow({ label, zone_id, point_name, value, unit, decimals, min, max }) {
    const [ data, setData ] = useState(value)
    const { PostData } = useZones()

    function OnSliderChange(new_value){
        setData(new_value)
        PostData(zone_id, point_name, new_value)
    }

    const formatted = data !== undefined && data !== null
        ? (decimals !== undefined ? Number(data).toFixed(decimals) : data)
        : null
    const display = formatted != null ? `${formatted}${unit}` : '—'

    useEffect(()=> {
        setData(value);
    }, [value]);

    return (
        <div className="slider-row">
            <div className="slider-info stat-row">
                <span className="stat-label">{label}</span>
                <span className="stat-value">{display}</span>
            </div>
            <div className="slider">
                <Slider
                    value={data ?? 0}
                    onChange={(e, new_value) => OnSliderChange(new_value)}
                    aria-label="Temperature"
                    valueLabelFormat={data}
                    valueLabelDisplay="auto"
                    shiftStep={20}
                    step={10}
                    marks
                    min={min}
                    max={max}
                />
            </div>
        </div>
    )
}

