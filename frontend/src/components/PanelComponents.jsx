import { useState, useEffect } from 'react'
import { useZones } from "../hooks/useZones"
import { useAHU } from "../hooks/useAHU"
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

export function StatRow({ label, value, unit, decimals }) {
    const formatted = value !== undefined && value !== null
        ? (decimals !== undefined ? Number(value).toFixed(decimals) : value)
        : null
    const display = formatted != null ? `${formatted}${unit}` : '—'
    return (
        <div className="stat-row">
            <span className="stat-label">{label}</span>
            <span className="stat-value">{display}</span>
        </div>
    )
}

export function AdjustRow({ label, point_name, locked_point, value, unit, decimals, min, max }) {
    const [ data, setData ] = useState(value)
    const { PostData } = useAHU()

    function onPlus(){
        const newVal = data + 0.5
        if (max !== undefined && newVal > max) return
        setData(newVal)
        PostData(point_name, newVal)
        if(locked_point) PostData(locked_point, newVal)
    }

    function onMinus(){
        const newVal = data - 0.5
        if (min !== undefined && newVal < min) return
        setData(newVal)
        PostData(point_name, newVal)
        if(locked_point) PostData(locked_point, newVal)
    }

    const formatted = data !== undefined && data !== null
        ? (decimals !== undefined ? Number(data).toFixed(decimals) : data)
        : null
    const display = formatted != null ? `${formatted}${unit}` : '—'

    useEffect(()=> {
        setData(value);
    }, [value]);

    return (
        <div className="adjust-row">
            <div className="stat-row">
                <span className="stat-label">{label}</span>
                <span className="stat-value">{display}</span>
            </div>
            <div className="adjust-buttons">
                <button onClick={onMinus} disabled={min !== undefined && data <= min}>-</button>
                <button onClick={onPlus}  disabled={max !== undefined && data >= max}>+</button>
            </div>
        </div>
    )
}

export function SliderRow({ label, zone_id, point_name, value, unit, decimals, min, max }) {
    const [ data, setData ] = useState(value)
    const { PostData: PostZone } = useZones()
    const { PostData: PostAHU } = useAHU()

    function OnSliderChange(new_value){
        setData(new_value)
        if (zone_id !== undefined) {
            PostZone(zone_id, point_name, new_value)
        } else {
            PostAHU(point_name, new_value)
        }
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

