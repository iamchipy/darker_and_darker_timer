#SingleInstance Force

ttuia := [1300,800] ; tooltip ui ancher
outer_border := [915,1382,1120,1177]  ; clock>y12,x3,y6,x9
diameter := [outer_border[3]-outer_border[1],outer_border[2]-outer_border[4]]
scale := 0.95
radius := (diameter[1]+diameter[2])/4
circle := [outer_border[4]+radius,outer_border[1]+radius,radius*scale]  ;xyr


; RGBA (Red, Green, Blue, Alpha) = 199, 164, 100, 255
; HSB (Hue, Saturation, Brightness) = 38.8°, 49.7%, 78.0%
; CMYK (Cyan, Magenta, Yellow, Key) = 0.0%, 17.6%, 49.7%, 22.0%
; Hex (RGB, RGBA, ARGB) = #C7A464, #C7A464FF, #FFC7A464
; Decimal (RGB, RGBA, ARGB) = 13083748, -945527553, -3693468
; Cursor position (X, Y) = 1289, 1116
; c4a262
trigger_zone_color := 0xc4a262

coords_at_angle(x,y,radius,angle){
    ; x = x₀ + r * cos(A)
    ; y = y₀ + r * sin(A)
    ; A = degrees * radian
    ; pi := 3.141592653589793
    ; radian := 360/(2*pi)
    fac := 0.01745329252  ; degrees to radians (multi factor)
    return [x+radius * Cos(fac*angle),y+radius * Sin(fac*angle)]
}

; return an array of desired length of coordinates along the perimeter of a circle
; using an origin and radius
coords_of_circle(x,y,r,number_of_points:=12){
    
    points_array := []
    offset :=  90 ; this is to adjust for normal clock start at 12/north
    loop number_of_points {
        
        a := ((360/number_of_points)*A_Index)-offset
        ;ToolTip( A_Index " "  a,,,15)
        points_array.push(coords_at_angle(x,y,r,a))
    }
    return points_array
}

is_ui_visible(array_to_check, color, variance:= 5, search_size:= 0, display_mode:=0){
    saw_something := false
    loop array_to_check.Length {
        x1:=array_to_check[A_Index][1]-search_size
        y1:=array_to_check[A_Index][2]-search_size
        x2:=array_to_check[A_Index][1]+search_size
        y2:=array_to_check[A_Index][2]+search_size
        match := PixelSearch(&x,&y,x1,y1,x2,y2,color,variance)
        if display_mode == 0{
            tt_n_clear A_Index,array_to_check[A_Index][1],array_to_check[A_Index][2], A_Index
   
        }  
        if match{
            if display_mode == 1{
                tt_n_clear A_Index,array_to_check[A_Index][1],array_to_check[A_Index][2], A_Index   
            }  
            saw_something +=1
            return A_Index
        }
    }
    return saw_something
}

clear_tooltip_after(time:=1000,index:=0){
    if time > 0
        time:=time*-1
    SetTimer(()=>ToolTip("",,,index),time)
}

tt_n_clear(msg,x:=0,y:=0,index:=1,duration:=500){
    ToolTip(msg,x,y,index)
    clear_tooltip_after(duration,index)
}

send_space(msg,x:=0,y:=0,index:=1,duration:=500){
    sendevent("{Space down}")
    sleep 10
    sendevent("{Space up}")
    ToolTip(msg,x,y,index)
    clear_tooltip_after(duration,index)
}

wait_for_picking_ui(trigger_zone_color:=0xc4a262,timeout:=6000){
    clock_coords := coords_of_circle(circle[1],circle[2],circle[3])
    avg_times:= []
    start := A_TickCount 
    loop {
        ;  break after timeout
        if A_TickCount - start > timeout
            break

        ; logging
        ; logging_tick := A_TickCount

        ; check if visible
        currently_visible := is_ui_visible(clock_coords, trigger_zone_color,,1,1)

        ; logging
        ; avg_times.push(A_TickCount-logging_tick)
        ; tt_n_clear(Round(avg_list(avg_times)),100,100,15,10000)

        if currently_visible
            return currently_visible

    }
    return false
}

avg_list(arr){
    total := 0
    loop arr.length{
        total += arr[A_Index]
    }
    return total / arr.length
}

lockpick_assist(hotkey_pressed){
    tt_n_clear("O.O",ttuia[1],ttuia[2],17)
    currently_visible := wait_for_picking_ui()
    ; if nothing was seen exit
    if !currently_visible
        return
    counter_clockwise_hours_to_target := 11-currently_visible-1  ;Time on Clock from north/12
    ms_per_clock_hour := 1000/12
    pick_delay := counter_clockwise_hours_to_target*ms_per_clock_hour
    SetTimer(()=>send_space("PICKED",ttuia[1],ttuia[2],18),-1*pick_delay)


}


; EXEC section
HotIfWinActive("ahk_exe DungeonCrawler.exe")
Hotkey("~^f", lockpick_assist)
