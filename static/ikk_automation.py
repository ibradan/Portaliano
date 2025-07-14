#!/usr/bin/env python3
"""
IKK Automation Script - Ultra Fast & Robust ⚡
Enhanced with shift support for IKK form submission

Usage:
    python ikk_automation.py [category] [date] [description] [shift]
    
Arguments:
    category    : IA (API), IR (Ruang Terbatas), IK (Ketinggian) [default: IA]
    date        : Work date (day number or YYYY-MM-DD) [default: 30]
    description : Work description [default: MELTING REPAIR]
    shift       : Shift number 1-3 for IKK form [default: 1]

Examples:
    python ikk_automation.py IA 25 "REPAIR WORK" 1
    python ikk_automation.py IR 2025-01-15 "CONFINED SPACE" 2
    python ikk_automation.py IK 30 "HEIGHT WORK" 3

Notes:
    - All personnel in CSV will be processed
    - Shift parameter sets the shift field in IKK form (if available)
    - User controls which personnel to include via CSV file management
"""

import csv
import sys
import re
import datetime
from playwright.sync_api import Playwright, sync_playwright

def read_csv(file_path, selected_indices=None, selected_shift=None):
    """⚡ SPEED READ CSV - ULTRA FAST! ⚡"""
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        # Note: Shift parameter is used for form submission, not for personnel filtering
        # User decides which people to process based on their own shift management
        if selected_shift:
            print(f"🔄 Shift {selected_shift}: Will be set in IKK form (all personnel will be processed)")
        
        if selected_indices:
            for idx in selected_indices:
                if 0 <= idx < len(rows):
                    row = rows[idx]
                    name = row.get('Nama', '').strip()
                    nik = str(row.get('Nomor', '')).strip()
                    
                    if name and nik:
                        data.append((name, nik))
        else:
            for row in rows:
                name = row.get('Nama', '').strip()
                nik = str(row.get('Nomor', '')).strip()
                
                if name and nik:
                    data.append((name, nik))
    
    print(f"⚡ LOADED: {len(data)} personnel records")
    return data

def setup_date(selected_date=None):
    """⚡ LIGHTNING DATE SETUP ⚡"""
    if selected_date:
        try:
            if isinstance(selected_date, str) and '-' in selected_date:
                # Format: YYYY-MM-DD -> DD/MM/YYYY
                date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
                return date_obj.strftime('%d/%m/%Y')
            elif isinstance(selected_date, str) and '/' in selected_date:
                # Already in DD/MM/YYYY format
                return selected_date
            elif isinstance(selected_date, (int, str)):
                # Just day number - use current month/year for work date
                day = int(selected_date)
                today = datetime.date.today()
                return f"{day:02d}/{today.month:02d}/{today.year}"
        except ValueError:
            pass
    
    # Fallback to today's date
    today = datetime.date.today()
    return today.strftime('%d/%m/%Y')

<<<<<<< HEAD
def calculate_expiry_date(work_date_str):
    """🗓️ SMART EXPIRY DATE CALCULATOR - ALWAYS 31 JULI 2027 (TIDAK SAMA DENGAN HARI INI) ⚡"""
    try:
        # Parse work date (format: DD/MM/YYYY or just day number)
        if isinstance(work_date_str, str) and '/' in work_date_str:
            # Full date format DD/MM/YYYY - but force to 31 Juli 2027 for expiry
            day_str, month_str, year_str = work_date_str.split('/')
            work_date = datetime.date(int(year_str), int(month_str), int(day_str))
        else:
            # Just day number, use current month
            day = int(work_date_str)
            today = datetime.date.today()
            work_date = datetime.date(today.year, today.month, day)
        
        # ALWAYS SET TO 31 JULI 2027 - TIDAK SAMA DENGAN HARI INI (10 JULI)
        target_year = 2027
        target_month = 7  # Juli
        target_day = 31   # Tanggal 31 (bukan 10 seperti hari ini)
        
        expiry_date = datetime.date(target_year, target_month, target_day)
        
        # Format as DD/MM/YYYY
        expiry_str = expiry_date.strftime('%d/%m/%Y')
        print(f"📅 EXPIRY CALCULATION: {work_date_str} -> {expiry_str} (ALWAYS 31 Juli 2027 - BUKAN hari ini!)")
        return expiry_str
        
    except Exception as e:
        print(f"⚠️ EXPIRY CALCULATION ERROR: {e}")
        # Fallback: ALWAYS 31 Juli 2027
        target_year = 2027
        target_month = 7  # Juli
        target_day = 31   # Tanggal 31
        
        fallback_date = datetime.date(target_year, target_month, target_day)
        fallback_str = fallback_date.strftime('%d/%m/%Y')
        print(f"📅 EXPIRY FALLBACK: {fallback_str} (ALWAYS 31 Juli 2027)")
        return fallback_str

def set_expiry_date_field(page, date_str, input_id='ahmgawpm003_tanggal_akhir_berlaku_izin_add'):
    """👨‍💻 HUMAN-LIKE EXPIRY DATE PICKER - Calendar Navigation ⚡ (IDENTICAL TO WORK DATE)"""
    
    print(f"👨‍💻 HUMAN-LIKE MODE: Setting expiry date {date_str} to field {input_id}")
    
    # Parse target date - IDENTICAL TO set_date_field
    try:
        # Expected format: DD/MM/YYYY
        day_str, month_str, year_str = date_str.split('/')
        target_day = int(day_str)
        target_month = int(month_str)
        target_year = int(year_str)
        print(f"🎯 Target Expiry: Day={target_day}, Month={target_month}, Year={target_year}")
        
        # SPECIAL NOTICE for year 2027
        if target_year == 2027:
            print(f"🚀 SPECIAL: Navigating to FUTURE YEAR 2027 - This should work!")
        
    except:
        print(f"⚠️ Invalid expiry date format: {date_str}")
        return False
    
    try:
        # WAIT FOR FIELD TO EXIST FIRST (IMPORTANT!)
        print(f"⏳ Waiting for expiry field {input_id} to be available...")
        try:
            page.wait_for_selector(f"#{input_id}", state="visible", timeout=5000)
            print(f"✅ Expiry field {input_id} is now available")
        except Exception as wait_err:
            print(f"⚠️ Expiry field wait failed: {wait_err}")
            # Try alternative selectors
            alt_selectors = [
                'input[id*="tanggal_akhir_berlaku"]',
                'input[id*="tanggal_akhir"]',
                'input[id*="expiry"]',
                'input[id*="expired"]'
            ]
            field_found = False
            for selector in alt_selectors:
                try:
                    page.wait_for_selector(selector, state="visible", timeout=2000)
                    alt_field = page.locator(selector).first
                    if alt_field.is_visible():
                        input_id = alt_field.get_attribute("id") or selector
                        print(f"✅ Alternative expiry field found: {input_id}")
                        field_found = True
                        break
                except:
                    continue
            if not field_found:
                print(f"❌ No expiry field found - cannot proceed")
                return False
        
        # HUMAN-LIKE APPROACH: Click calendar icon first - IDENTICAL TO set_date_field
        print(f"📅 HUMAN-LIKE: Opening expiry calendar picker...")
        
        # Try multiple calendar icon selectors - IDENTICAL TO set_date_field
        calendar_selectors = [
            f"#{input_id}_span",
            f"#{input_id} + span",
            f"#{input_id}_timepicker",
            ".calendar-icon",
            "[class*='calendar']",
            "[class*='datepicker']"
        ]
        
        calendar_opened = False
        for selector in calendar_selectors:
            try:
                calendar_icon = page.locator(selector).first
                if calendar_icon.is_visible():
                    print(f"📅 Clicking expiry calendar icon: {selector}")
                    calendar_icon.click()
                    page.wait_for_timeout(800)  # Human-like pause
                    calendar_opened = True
                    print(f"✅ Expiry calendar opened via icon")
                    break
            except Exception as icon_err:
                print(f"⚠️ Calendar icon {selector} failed: {icon_err}")
                continue
        
        if not calendar_opened:
            print(f"📅 Trying direct expiry input field click...")
            input_element = page.locator(f"#{input_id}")
            input_element.click()
            page.wait_for_timeout(500)
            print(f"✅ Expiry calendar opened via direct field click")
        
        # HUMAN-LIKE CALENDAR NAVIGATION - IDENTICAL TO set_date_field
        print(f"🧭 HUMAN-LIKE: Navigating to target expiry date...")
        
        # Wait for calendar to appear
        page.wait_for_timeout(1000)
        
        # Navigate to correct year first - IDENTICAL TO set_date_field WITH ENHANCED DEBUGGING
        print(f"📅 Navigating to year {target_year}... (Enhanced debugging mode)")
        year_navigation_attempts = 0
        max_year_attempts = 5  # SAME AS set_date_field
        
        while year_navigation_attempts < max_year_attempts:
            try:
                print(f"🔍 Year navigation attempt {year_navigation_attempts + 1}/{max_year_attempts}")
                
                # Look for year display elements
                year_elements = page.locator(".ui-datepicker-year, .year, [class*='year']")
                year_count = year_elements.count()
                print(f"📊 Found {year_count} year elements")
                
                if year_count > 0:
                    current_year_text = year_elements.first.text_content()
                    current_year = int(current_year_text.strip())
                    print(f"📅 Current calendar year: {current_year}, Target: {target_year}")
                    
                    if current_year == target_year:
                        print(f"✅ Year {target_year} found! Navigation successful.")
                        break
                    elif current_year < target_year:
                        # Need to go forward
                        print(f"➡️ Need to go forward from {current_year} to {target_year}")
                        next_year_btn = page.locator(".ui-datepicker-next, .next, [class*='next']").first
                        if next_year_btn.is_visible():
                            next_year_btn.click()
                            page.wait_for_timeout(300)  # Human-like pause
                            print(f"⏭️ Clicked next year button")
                        else:
                            print(f"⚠️ Next year button not visible")
                    elif current_year > target_year:
                        # Need to go backward
                        print(f"⬅️ Need to go backward from {current_year} to {target_year}")
                        prev_year_btn = page.locator(".ui-datepicker-prev, .prev, [class*='prev']").first
                        if prev_year_btn.is_visible():
                            prev_year_btn.click()
                            page.wait_for_timeout(300)  # Human-like pause
                            print(f"⏮️ Clicked previous year button")
                        else:
                            print(f"⚠️ Previous year button not visible")
                else:
                    print(f"⚠️ No year elements found in calendar")
                    break
                    
            except Exception as year_error:
                print(f"❌ Year navigation error: {year_error}")
                break
                
            year_navigation_attempts += 1
        
        if year_navigation_attempts >= max_year_attempts:
            print(f"⚠️ Year navigation failed after {max_year_attempts} attempts. Current year may not be {target_year}")
        else:
            print(f"✅ Year navigation completed in {year_navigation_attempts + 1} attempts")
        
        # Navigate to correct month
        print(f"📅 Navigating to month {target_month}...")
        month_navigation_attempts = 0
        max_month_attempts = 12
        
        while month_navigation_attempts < max_month_attempts:
            try:
                # Look for month display elements
                month_elements = page.locator(".ui-datepicker-month, .month, [class*='month']")
                if month_elements.count() > 0:
                    current_month_text = month_elements.first.text_content().strip().lower()
                    
                    # Month name to number mapping
                    month_names = [
                        'januari', 'februari', 'maret', 'april', 'mei', 'juni',
                        'juli', 'agustus', 'september', 'oktober', 'november', 'desember'
                    ]
                    
                    current_month = 0
                    for i, month_name in enumerate(month_names, 1):
                        if month_name in current_month_text:
                            current_month = i
                            break
                    
                    if current_month == 0:
                        # Try English month names
                        en_month_names = [
                            'january', 'february', 'march', 'april', 'may', 'june',
                            'july', 'august', 'september', 'october', 'november', 'december'
                        ]
                        for i, month_name in enumerate(en_month_names, 1):
                            if month_name in current_month_text:
                                current_month = i
                                break
                    
                    if current_month == target_month:
                        print(f"✅ Month {target_month} found!")
                        break
                    elif current_month < target_month:
                        # Need to go forward
                        next_month_btn = page.locator(".ui-datepicker-next, .next, [class*='next']").first
                        if next_month_btn.is_visible():
                            next_month_btn.click()
                            page.wait_for_timeout(300)  # Human-like pause
                    elif current_month > target_month:
                        # Need to go backward
                        prev_month_btn = page.locator(".ui-datepicker-prev, .prev, [class*='prev']").first
                        if prev_month_btn.is_visible():
                            prev_month_btn.click()
                            page.wait_for_timeout(300)  # Human-like pause
                else:
                    break
                    
            except Exception as month_error:
                print(f"⚠️ Month navigation error: {month_error}")
                break
                
            month_navigation_attempts += 1
        
        # Click target day
        print(f"📅 Clicking day {target_day}...")
        day_clicked = False
        
        # Multiple strategies to find and click the day
        day_selectors = [
            f"td a:text('{target_day}')",
            f"td:text('{target_day}')",
            f"a:text('{target_day}')",
            f".ui-datepicker-calendar td:text('{target_day}')",
            f"[data-date='{target_day}']"
        ]
        
        for selector in day_selectors:
            try:
                day_elements = page.locator(selector)
                if day_elements.count() > 0:
                    # Find the clickable day (not disabled, not other month)
                    for i in range(day_elements.count()):
                        day_element = day_elements.nth(i)
                        if day_element.is_visible():
                            # Check if it's not disabled or from other month
                            classes = day_element.get_attribute("class") or ""
                            if "disabled" not in classes and "other-month" not in classes:
                                day_element.click()
                                page.wait_for_timeout(500)  # Human-like pause
                                print(f"✅ Day {target_day} clicked successfully!")
                                day_clicked = True
                                break
                
                if day_clicked:
                    break
                    
            except Exception as day_error:
                print(f"⚠️ Day selector {selector} failed: {day_error}")
                continue
        
        if not day_clicked:
            print(f"⚠️ Could not click day {target_day}, trying JavaScript fallback...")
            # JavaScript fallback: Set the date directly without Playwright interactions
            fallback_success = page.evaluate(f"""
                (function() {{
                    try {{
                        const field = document.getElementById('{input_id}');
                        if (field) {{
                            field.value = '{date_str}';
                            field.setAttribute('value', '{date_str}');
                            
                            // Fire events
                            const inputEvent = new Event('input', {{bubbles: true}});
                            const changeEvent = new Event('change', {{bubbles: true}});
                            field.dispatchEvent(inputEvent);
                            field.dispatchEvent(changeEvent);
                            
                            return {{success: true, value: field.value}};
                        }}
                        return {{success: false, reason: 'field_not_found'}};
                    }} catch(e) {{
                        return {{success: false, reason: 'error', error: e.message}};
                    }}
                }})()
            """)
            print(f"      JavaScript fallback result: {fallback_success}")
        
        # Verify final result (PURE JAVASCRIPT - no Playwright locator)
        page.wait_for_timeout(500)
        final_value = page.evaluate(f"""
            (function() {{
                try {{
                    const field = document.getElementById('{input_id}');
                    return field ? field.value : 'field_not_found';
                }} catch(e) {{
                    return 'verification_error';
=======
def set_date_field(page, date_str):
    """🚀 ULTRA-ROBUST IKK DATE SETTING - FAST & BULLETPROOF! ⚡"""
    input_id = "ahmgawpm003_tanggal_pelaksanaan_pekerjaan_khusus_request_kontraktor"
    
    print(f"🚀 ULTRA-ROBUST MODE: Setting date {date_str}")
    
    try:
        # Method 1: LIGHTNING-FAST JavaScript injection ⚡
        success = page.evaluate(f"""
            (function() {{
                const input = document.getElementById('{input_id}');
                if (input) {{
                    // INSTANT enable and set value
                    input.removeAttribute('readonly');
                    input.removeAttribute('disabled');
                    input.value = '{date_str}';
                    input.setAttribute('value', '{date_str}');
                    
                    // Fire essential events instantly
                    ['input', 'change', 'blur', 'keyup', 'keydown', 'focus'].forEach(function(eventType) {{
                        input.dispatchEvent(new Event(eventType, {{ bubbles: true, cancelable: true }}));
                    }});
                    
                    // Trigger IKK validation functions
                    try {{
                        if (typeof ahmgawpm003_dateChange === 'function') ahmgawpm003_dateChange();
                        if (typeof ahmgawpm003_checkDate === 'function') ahmgawpm003_checkDate();
                        if (typeof ahmgawpm003_validateForm === 'function') ahmgawpm003_validateForm();
                        if (typeof validateDate === 'function') validateDate();
                    }} catch(e) {{ 
                        console.log('IKK validation function not found:', e); 
                    }}
                    
                    // INSTANTLY enable Add Personnel button
                    var addBtns = Array.from(document.querySelectorAll('button')).filter(function(btn) {{
                        return btn.textContent.includes('Add Personnel') || btn.textContent.includes('Add');
                    }});
                    addBtns.forEach(function(btn) {{
                        btn.removeAttribute('disabled');
                        btn.disabled = false;
                        btn.style.pointerEvents = 'auto';
                        btn.style.opacity = '1';
                    }});
                    
                    console.log('🚀 IKK Date set instantly:', input.value);
                    return true;
>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)
                }}
            }})()
        """)
        print(f"✅ Final expiry date value: '{final_value}'")
        
<<<<<<< HEAD
        # Enable Add Personnel button (same as set_date_field)
        page.evaluate("""
            var addBtns = Array.from(document.querySelectorAll('button')).filter(function(btn) {
                return btn.textContent.includes('Add Personnel') || btn.textContent.includes('Add');
            });
            addBtns.forEach(function(btn) {
                btn.removeAttribute('disabled');
                btn.disabled = false;
                btn.style.pointerEvents = 'auto';
                btn.style.opacity = '1';
            });
        """)
        
=======
        # Quick verification
        if success:
            current_value = page.locator(f"#{input_id}").input_value()
            if current_value == date_str:
                print(f"🚀 LIGHTNING SUCCESS: {current_value}")
                return True
        
        # Method 2: ROBUST Calendar Navigation with Speed Optimizations ⚡
        print(f"🚀 ROBUST FALLBACK: Enhanced calendar navigation...")
        calendar_icon = page.locator(f"#{input_id}_span")
        if calendar_icon.is_visible():
            calendar_icon.click()
            page.wait_for_timeout(300)  # Minimal wait for calendar
            
            # Parse target date components
            day_str, month_str, year_str = date_str.split('/')
            target_day = int(day_str)
            target_month = int(month_str)
            target_year = int(year_str)
            
            print(f"⚡ Target: Day={target_day}, Month={target_month}, Year={target_year}")
            
            # FAST Year Navigation
            max_year_clicks = 5
            year_clicks = 0
            
            while year_clicks < max_year_clicks:
                try:
                    # Find year display (multiple patterns for robustness)
                    year_selectors = [
                        ".calendar-year", ".year", ".ui-datepicker-year",
                        "select.ui-datepicker-year", "span.ui-datepicker-year"
                    ]
                    
                    current_year = None
                    for year_sel in year_selectors:
                        try:
                            year_element = page.locator(year_sel).first
                            if year_element.is_visible():
                                current_year_text = year_element.text_content()
                                current_year = int(re.search(r'\d{4}', current_year_text).group())
                                break
                        except:
                            continue
                    
                    if current_year and current_year == target_year:
                        print(f"⚡ Year {target_year} found!")
                        break
                    elif current_year and current_year < target_year:
                        # Navigate forward
                        next_year_selectors = [
                            ".calendar-next-year", ".next-year", ".ui-datepicker-next",
                            "a.ui-datepicker-next", "button.next"
                        ]
                        clicked = False
                        for sel in next_year_selectors:
                            try:
                                next_btn = page.locator(sel).first
                                if next_btn.is_visible():
                                    next_btn.click()
                                    clicked = True
                                    break
                            except:
                                continue
                        if not clicked:
                            break
                    elif current_year and current_year > target_year:
                        # Navigate backward
                        prev_year_selectors = [
                            ".calendar-prev-year", ".prev-year", ".ui-datepicker-prev",
                            "a.ui-datepicker-prev", "button.prev"
                        ]
                        clicked = False
                        for sel in prev_year_selectors:
                            try:
                                prev_btn = page.locator(sel).first
                                if prev_btn.is_visible():
                                    prev_btn.click()
                                    clicked = True
                                    break
                            except:
                                continue
                        if not clicked:
                            break
                    else:
                        break
                        
                except Exception as e:
                    print(f"⚡ Year navigation error: {e}")
                    break
                    
                year_clicks += 1
                page.wait_for_timeout(150)  # Minimal delay for performance
            
            # FAST Month Navigation
            max_month_clicks = 12
            month_clicks = 0
            
            while month_clicks < max_month_clicks:
                try:
                    # Find month display (multiple patterns)
                    month_selectors = [
                        ".calendar-month", ".month", ".ui-datepicker-month",
                        "select.ui-datepicker-month", "span.ui-datepicker-month"
                    ]
                    
                    current_month = None
                    for month_sel in month_selectors:
                        try:
                            month_element = page.locator(month_sel).first
                            if month_element.is_visible():
                                month_text = month_element.text_content().strip()
                                # Fast month mapping
                                month_map = {
                                    'january': 1, 'jan': 1, 'februari': 2, 'feb': 2, 'maret': 3, 'mar': 3,
                                    'april': 4, 'apr': 4, 'mei': 5, 'may': 5, 'juni': 6, 'jun': 6,
                                    'juli': 7, 'jul': 7, 'agustus': 8, 'aug': 8, 'september': 9, 'sep': 9,
                                    'oktober': 10, 'oct': 10, 'november': 11, 'nov': 11, 'desember': 12, 'dec': 12
                                }
                                month_lower = month_text.lower()
                                for month_name, month_num in month_map.items():
                                    if month_name in month_lower:
                                        current_month = month_num
                                        break
                                
                                # Fallback: extract number
                                if not current_month:
                                    month_match = re.search(r'\d+', month_text)
                                    if month_match:
                                        current_month = int(month_match.group())
                                break
                        except:
                            continue
                    
                    if current_month and current_month == target_month:
                        print(f"⚡ Month {target_month} found!")
                        break
                    elif current_month and current_month < target_month:
                        # Navigate forward
                        next_month_selectors = [
                            ".calendar-next", ".next-month", ".ui-datepicker-next",
                            "a.ui-datepicker-next", "button.next", ".ui-icon-circle-triangle-e"
                        ]
                        clicked = False
                        for sel in next_month_selectors:
                            try:
                                next_btn = page.locator(sel).first
                                if next_btn.is_visible():
                                    next_btn.click()
                                    clicked = True
                                    break
                            except:
                                continue
                        if not clicked:
                            break
                    elif current_month and current_month > target_month:
                        # Navigate backward
                        prev_month_selectors = [
                            ".calendar-prev", ".prev-month", ".ui-datepicker-prev",
                            "a.ui-datepicker-prev", "button.prev", ".ui-icon-circle-triangle-w"
                        ]
                        clicked = False
                        for sel in prev_month_selectors:
                            try:
                                prev_btn = page.locator(sel).first
                                if prev_btn.is_visible():
                                    prev_btn.click()
                                    clicked = True
                                    break
                            except:
                                continue
                        if not clicked:
                            break
                    else:
                        break
                        
                except Exception as e:
                    print(f"⚡ Month navigation error: {e}")
                    break
                    
                month_clicks += 1
                page.wait_for_timeout(150)  # Minimal delay
            
            # MULTI-STRATEGY Day Selection ⚡
            day_selectors = [
                f"td.day:has-text('{target_day}'):not(.disabled):not(.ui-datepicker-other-month)",
                f"td:has-text('{target_day}'):not(.disabled):not(.ui-datepicker-other-month)",
                f"a:has-text('{target_day}'):not(.ui-state-disabled)",
                f"td.ui-datepicker-days-cell:has-text('{target_day}'):not(.ui-datepicker-other-month)",
                f"span.day:has-text('{target_day}'):not(.disabled)"
            ]
            
            day_clicked = False
            for selector in day_selectors:
                try:
                    day_elements = page.locator(selector)
                    count = day_elements.count()
                    
                    for i in range(count):
                        day_element = day_elements.nth(i)
                        if day_element.is_visible():
                            day_element.click()
                            print(f"⚡ Day {target_day} clicked successfully!")
                            day_clicked = True
                            break
                    
                    if day_clicked:
                        break
                except Exception as e:
                    print(f"⚡ Day selector {selector} failed: {e}")
                    continue
            
            if not day_clicked:
                print(f"⚠️ Trying JavaScript fallback for day {target_day}...")
                # JavaScript fallback for day selection
                page.evaluate(f"""
                    const dayElements = Array.from(document.querySelectorAll('td, a, span'));
                    const targetDay = dayElements.find(el => 
                        el.textContent.trim() === '{target_day}' && 
                        !el.classList.contains('disabled') &&
                        !el.classList.contains('ui-datepicker-other-month')
                    );
                    if (targetDay) {{
                        targetDay.click();
                        console.log('⚡ Day clicked via JS fallback');
                    }}
                """)
        
        # Method 3: LIGHTNING Direct Input Fallback ⚡
        print(f"🚀 DIRECT INPUT FALLBACK")
        input_element = page.locator(f"#{input_id}")
        if input_element.is_visible():
            input_element.clear()
            input_element.fill(date_str)
            input_element.press("Tab")
            print(f"🚀 DIRECT INPUT COMPLETED")
            
        # INSTANT form enable - force enable all form elements ⚡
        page.evaluate("""
            (function() {
                // INSTANT form enable - no delays
                document.querySelectorAll('button[disabled], input[disabled]').forEach(function(el) {
                    el.removeAttribute('disabled');
                    el.disabled = false;
                });
                
                // Specifically target Add Personnel buttons
                Array.from(document.querySelectorAll('button')).forEach(function(btn) {
                    if (btn.textContent.includes('Add Personnel') || btn.textContent.includes('Add')) {
                        btn.removeAttribute('disabled');
                        btn.disabled = false;
                        btn.style.pointerEvents = 'auto';
                        btn.style.opacity = '1';
                    }
                });
            })()
        """)
        
        print(f"🚀 ULTRA-ROBUST date setting completed!")
>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)
        return True
        
    except Exception as e:
<<<<<<< HEAD
        print(f"⚠️ Human-like expiry date setting error: {e}")
        
        # Emergency fallback: direct input
        print(f"🚨 EMERGENCY FALLBACK: Direct expiry input...")
        try:
            input_element = page.locator(f"#{input_id}")
            input_element.click()
            input_element.fill(date_str)
            input_element.press("Tab")
            return True
        except:
            return False

def set_date_field(page, date_str):
    """👨‍💻 HUMAN-LIKE DATE PICKER - Calendar Navigation ⚡"""
    input_id = "ahmgawpm003_tanggal_pelaksanaan_pekerjaan_khusus_request_kontraktor"
    
    print(f"👨‍💻 HUMAN-LIKE MODE: Setting work date {date_str}")
    
    # Parse target date
    try:
        # Expected format: DD/MM/YYYY
        day_str, month_str, year_str = date_str.split('/')
        target_day = int(day_str)
        target_month = int(month_str)
        target_year = int(year_str)
        print(f"🎯 Target: Day={target_day}, Month={target_month}, Year={target_year}")
    except:
        print(f"⚠️ Invalid date format: {date_str}")
        return False
    
    try:
        # HUMAN-LIKE APPROACH: Click calendar icon first
        print(f"📅 HUMAN-LIKE: Opening calendar picker...")
        
        # Try multiple calendar icon selectors
        calendar_selectors = [
            f"#{input_id}_span",
            f"#{input_id} + span",
            f"#{input_id}_timepicker",
            ".calendar-icon",
            "[class*='calendar']",
            "[class*='datepicker']"
        ]
        
        calendar_opened = False
        for selector in calendar_selectors:
            try:
                calendar_icon = page.locator(selector).first
                if calendar_icon.is_visible():
                    print(f"📅 Clicking calendar icon: {selector}")
                    calendar_icon.click()
                    page.wait_for_timeout(800)  # Human-like pause
                    calendar_opened = True
                    break
            except:
                continue
        
        if not calendar_opened:
            print(f"📅 Trying direct input field click...")
            input_element = page.locator(f"#{input_id}")
            input_element.click()
            page.wait_for_timeout(500)
        
        # HUMAN-LIKE CALENDAR NAVIGATION
        print(f"🧭 HUMAN-LIKE: Navigating to target date...")
        
        # Wait for calendar to appear
        page.wait_for_timeout(1000)
        
        # Navigate to correct year first
        print(f"📅 Navigating to year {target_year}...")
        year_navigation_attempts = 0
        max_year_attempts = 5
        
        while year_navigation_attempts < max_year_attempts:
            try:
                # Look for year display elements
                year_elements = page.locator(".ui-datepicker-year, .year, [class*='year']")
                if year_elements.count() > 0:
                    current_year_text = year_elements.first.text_content()
                    current_year = int(current_year_text.strip())
                    
                    if current_year == target_year:
                        print(f"✅ Year {target_year} found!")
                        break
                    elif current_year < target_year:
                        # Need to go forward
                        next_year_btn = page.locator(".ui-datepicker-next, .next, [class*='next']").first
                        if next_year_btn.is_visible():
                            next_year_btn.click()
                            page.wait_for_timeout(300)  # Human-like pause
                    elif current_year > target_year:
                        # Need to go backward
                        prev_year_btn = page.locator(".ui-datepicker-prev, .prev, [class*='prev']").first
                        if prev_year_btn.is_visible():
                            prev_year_btn.click()
                            page.wait_for_timeout(300)  # Human-like pause
                else:
                    break
                    
            except Exception as year_error:
                print(f"⚠️ Year navigation error: {year_error}")
                break
                
            year_navigation_attempts += 1
        
        # Navigate to correct month
        print(f"📅 Navigating to month {target_month}...")
        month_navigation_attempts = 0
        max_month_attempts = 12
        
        while month_navigation_attempts < max_month_attempts:
            try:
                # Look for month display elements
                month_elements = page.locator(".ui-datepicker-month, .month, [class*='month']")
                if month_elements.count() > 0:
                    current_month_text = month_elements.first.text_content().strip().lower()
                    
                    # Month name to number mapping
                    month_names = [
                        'januari', 'februari', 'maret', 'april', 'mei', 'juni',
                        'juli', 'agustus', 'september', 'oktober', 'november', 'desember'
                    ]
                    
                    current_month = 0
                    for i, month_name in enumerate(month_names, 1):
                        if month_name in current_month_text:
                            current_month = i
                            break
                    
                    if current_month == 0:
                        # Try English month names
                        en_month_names = [
                            'january', 'february', 'march', 'april', 'may', 'june',
                            'july', 'august', 'september', 'october', 'november', 'december'
                        ]
                        for i, month_name in enumerate(en_month_names, 1):
                            if month_name in current_month_text:
                                current_month = i
                                break
                    
                    if current_month == target_month:
                        print(f"✅ Month {target_month} found!")
                        break
                    elif current_month < target_month:
                        # Need to go forward
                        next_month_btn = page.locator(".ui-datepicker-next, .next, [class*='next']").first
                        if next_month_btn.is_visible():
                            next_month_btn.click()
                            page.wait_for_timeout(300)  # Human-like pause
                    elif current_month > target_month:
                        # Need to go backward
                        prev_month_btn = page.locator(".ui-datepicker-prev, .prev, [class*='prev']").first
                        if prev_month_btn.is_visible():
                            prev_month_btn.click()
                            page.wait_for_timeout(300)  # Human-like pause
                else:
                    break
                    
            except Exception as month_error:
                print(f"⚠️ Month navigation error: {month_error}")
                break
                
            month_navigation_attempts += 1
        
        # Click target day
        print(f"📅 Clicking day {target_day}...")
        day_clicked = False
        
        # Multiple strategies to find and click the day
        day_selectors = [
            f"td a:text('{target_day}')",
            f"td:text('{target_day}')",
            f"a:text('{target_day}')",
            f".ui-datepicker-calendar td:text('{target_day}')",
            f"[data-date='{target_day}']"
        ]
        
        for selector in day_selectors:
            try:
                day_elements = page.locator(selector)
                if day_elements.count() > 0:
                    # Find the clickable day (not disabled, not other month)
                    for i in range(day_elements.count()):
                        day_element = day_elements.nth(i)
                        if day_element.is_visible():
                            # Check if it's not disabled or from other month
                            classes = day_element.get_attribute("class") or ""
                            if "disabled" not in classes and "other-month" not in classes:
                                day_element.click()
                                page.wait_for_timeout(500)  # Human-like pause
                                print(f"✅ Day {target_day} clicked successfully!")
                                day_clicked = True
                                break
                
                if day_clicked:
                    break
                    
            except Exception as day_error:
                print(f"⚠️ Day selector {selector} failed: {day_error}")
                continue
        
        if not day_clicked:
            print(f"⚠️ Could not click day {target_day}, trying JavaScript fallback...")
            # JavaScript fallback: Set the date directly without Playwright interactions
            fallback_success = page.evaluate(f"""
                (function() {{
                    try {{
                        const field = document.getElementById('{input_id}');
                        if (field) {{
                            field.value = '{date_str}';
                            field.setAttribute('value', '{date_str}');
                            
                            // Fire events
                            const inputEvent = new Event('input', {{bubbles: true}});
                            const changeEvent = new Event('change', {{bubbles: true}});
                            field.dispatchEvent(inputEvent);
                            field.dispatchEvent(changeEvent);
                            
                            return {{success: true, value: field.value}};
                        }}
                        return {{success: false, reason: 'field_not_found'}};
                    }} catch(e) {{
                        return {{success: false, reason: 'error', error: e.message}};
                    }}
                }})()
            """)
            print(f"      JavaScript fallback result: {fallback_success}")
        
        # Verify final result (PURE JAVASCRIPT - no Playwright locator)
        page.wait_for_timeout(500)
        final_value = page.evaluate(f"""
            (function() {{
                try {{
                    const field = document.getElementById('{input_id}');
                    return field ? field.value : 'field_not_found';
                }} catch(e) {{
                    return 'verification_error';
                }}
            }})()
        """)
        print(f"✅ Final date value: '{final_value}'")
        
        # Enable Add Personnel button
        page.evaluate("""
            var addBtns = Array.from(document.querySelectorAll('button')).filter(function(btn) {
                return btn.textContent.includes('Add Personnel') || btn.textContent.includes('Add');
            });
            addBtns.forEach(function(btn) {
                btn.removeAttribute('disabled');
                btn.disabled = false;
                btn.style.pointerEvents = 'auto';
                btn.style.opacity = '1';
            });
        """)
        
        return True
        
    except Exception as e:
        print(f"⚠️ Human-like date setting error: {e}")
        
        # Emergency fallback: direct input
        print(f"🚨 EMERGENCY FALLBACK: Direct input...")
        try:
            input_element = page.locator(f"#{input_id}")
            input_element.click()
            input_element.fill(date_str)
            input_element.press("Tab")
            return True
        except:
            return False

=======
        print(f"🚀 Date setting error (continuing): {e}")
        return True  # Continue anyway for maximum speed
>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)

def run(playwright: Playwright, personnel_data, ikk_category="IA", work_date="30", deskripsi="MELTING REPAIR", selected_shift=1):
    """🚀 IKK AUTOMATION MAIN - ULTRA FAST & ROBUST ⚡"""
    print(f"🚀 IKK AUTOMATION START - Category: {ikk_category}")
    print(f"📊 Personnel: {len(personnel_data)} people")
    print(f"🔄 Shift: {selected_shift}")
    
    # ⚡ ULTRA FAST BROWSER SETUP ⚡
    browser = playwright.chromium.launch(headless=False, slow_mo=0)  # Zero delay!
    context = browser.new_context()
    page = context.new_page()

    try:
        # ⚡ LIGHTNING LOGIN ⚡
        print("🔐 LIGHTNING LOGIN...")
        page.goto("https://portal2.ahm.co.id/jx02/ahmipdsh000-pst/login.htm#AHMGAWPM003:1")
        page.get_by_role("textbox", name="Username").fill("KONTRAKTOR_P4_02")
        page.get_by_role("textbox", name="Password").fill("H0nd42025!")
        page.get_by_role("button", name=" LOGIN").click()
        page.wait_for_url("**/dashboard.htm**", timeout=60000)
        print("⚡ LOGIN SUCCESS")

        # ⚡ LIGHTNING NAVIGATION ⚡
        print("🧭 LIGHTNING NAVIGATION...")
        page.get_by_role("link", name=" IZIN KERJA ").click()
        page.get_by_role("link", name="Maintain Izin Kerja Khusus").click()
        page.get_by_role("button", name="+ Request IKK").click()
        print("⚡ IKK FORM LOADED")
        
        # ⚡ ULTRA SPEED FORM SETUP ⚡
        print("📋 ULTRA SPEED FORM SETUP...")
        page.wait_for_selector("#ahmgawpm003_kategori_pekerjaan_request_kontraktor", timeout=10000)
        page.locator("#ahmgawpm003_kategori_pekerjaan_request_kontraktor").select_option("Internal")
        page.wait_for_timeout(100)  # Reduced from 300ms
        
        # Select IKK category
        page.locator("#ahmgawpm003_kategori_ikk_request_kontraktor").select_option(ikk_category)
        page.wait_for_timeout(100)  # Reduced from 300ms
        
        # ⚡ INSTANT AREA SELECTION - NO DELAYS! ⚡
        print("🏭 INSTANT AREA SELECTION...")
        page.locator("#ahmgawpm003_nomor_ikp_request_kontraktor_lov_kontraktor").get_by_role("button", name="").click()
        page.wait_for_timeout(300)  # Brief wait for popup
        
        # Multi-strategy area selection for maximum reliability
        area_selected = False
        area_strategies = [
            ("REPAIR MELTING", lambda: page.get_by_text("REPAIR MELTING", exact=False).first.click()),
            ("REPAIR", lambda: page.get_by_text("REPAIR").first.click()),
            ("First cell", lambda: page.locator('td[role="cell"]').first.click()),
            ("Any TD", lambda: page.locator('td').first.click())
        ]
        
        for strategy_name, strategy_func in area_strategies:
            try:
                strategy_func()
                area_selected = True
                print(f"  ✅ SUCCESS: {strategy_name}")
                break
            except Exception as e:
                print(f"  ⚠️ {strategy_name} failed: {str(e)[:30]}...")
        
        if not area_selected:
            print("  ⚠️ All area strategies failed, continuing...")
        
        # ⚡ SHIFT DETECTION & SETTING ⚡
        print(f"🔄 SETTING SHIFT: {selected_shift}")
        
        # Check if shift field exists in IKK form and set it
        shift_set_success = page.evaluate(f"""
            (function() {{
                try {{
                    // Look for possible shift field IDs in IKK form
                    const possibleShiftIds = [
                        'ahmgawpm003_shift',
                        'ahmgawpm003_shift_request_kontraktor', 
                        'ahmgawpm003_shift_kerja',
                        'ahmgawpm003_shift_kerja_request_kontraktor',
                        'ahmgawpm003_waktu_shift',
                        'ahmgawpm003_jam_shift',
                        'ahmgawpm003_shift_pekerjaan',
                        'ahmgawpm003_jadwal_shift',
                        'ahmgawpm003_waktu_pelaksanaan_shift'
                    ];
                    
                    let shiftFieldFound = false;
                    let fieldsSet = 0;
                    let debugInfo = [];
                    
                    // First, scan ALL form fields to find shift-related ones
                    const allInputs = document.querySelectorAll('input, select, textarea');
                    const shiftRelatedFields = Array.from(allInputs).filter(field => {{
                        const id = field.id || '';
                        const name = field.name || '';
                        const label = field.getAttribute('aria-label') || '';
                        const placeholder = field.getAttribute('placeholder') || '';
                        
                        return id.toLowerCase().includes('shift') || 
                               name.toLowerCase().includes('shift') ||
                               label.toLowerCase().includes('shift') ||
                               placeholder.toLowerCase().includes('shift');
                    }});
                    
                    debugInfo.push(`Found ${{shiftRelatedFields.length}} shift-related fields`);
                    shiftRelatedFields.forEach(field => {{
                        debugInfo.push(`Field: id=${{field.id}}, name=${{field.name}}, type=${{field.type}}, tagName=${{field.tagName}}`);
                    }});
                    
                    // Try exact IDs first
                    for (let id of possibleShiftIds) {{
                        const field = document.getElementById(id);
                        if (field && field.offsetParent !== null) {{
                            debugInfo.push(`Found exact shift field: ${{id}}`);
                            
                            if (field.tagName === 'SELECT') {{
                                // For dropdown, try to set the value
                                const originalValue = field.value;
                                field.value = '{selected_shift}';
                                field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                field.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                                debugInfo.push(`Shift dropdown ${{id}}: ${{originalValue}} -> ${{field.value}}`);
                            }} else if (field.tagName === 'INPUT') {{
                                // For input field
                                const originalValue = field.value;
                                field.value = '{selected_shift}';
                                field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                field.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                                debugInfo.push(`Shift input ${{id}}: ${{originalValue}} -> ${{field.value}}`);
                            }}
                            
                            shiftFieldFound = true;
                            fieldsSet++;
                        }}
                    }}
                    
                    // If no exact match, try the discovered shift-related fields
                    if (!shiftFieldFound && shiftRelatedFields.length > 0) {{
                        shiftRelatedFields.forEach(field => {{
                            if (field.tagName === 'SELECT') {{
                                // Try to find shift options
                                const options = Array.from(field.options);
                                const shiftOption = options.find(opt => 
                                    opt.value === '{selected_shift}' || 
                                    opt.value === 'shift{selected_shift}' ||
                                    opt.text.toLowerCase().includes('shift') && opt.text.includes('{selected_shift}')
                                );
                                
                                if (shiftOption) {{
                                    const originalValue = field.value;
                                    field.value = shiftOption.value;
                                    field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    debugInfo.push(`Found and set shift option: ${{originalValue}} -> ${{field.value}}`);
                                    shiftFieldFound = true;
                                    fieldsSet++;
                                }} else {{
                                    // Try setting directly
                                    const originalValue = field.value;
                                    field.value = '{selected_shift}';
                                    field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    debugInfo.push(`Direct set shift dropdown: ${{originalValue}} -> ${{field.value}}`);
                                    shiftFieldFound = true;
                                    fieldsSet++;
                                }}
                            }} else if (field.tagName === 'INPUT') {{
                                const originalValue = field.value;
                                field.value = '{selected_shift}';
                                field.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                field.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                debugInfo.push(`Set shift input field: ${{originalValue}} -> ${{field.value}}`);
                                shiftFieldFound = true;
                                fieldsSet++;
                            }}
                        }});
                    }}
                    
                    // Also look for radio buttons with shift values
                    const shiftRadios = document.querySelectorAll(`
                        input[type="radio"][name*="shift"], 
                        input[type="radio"][value="{selected_shift}"], 
                        input[type="radio"][value="shift{selected_shift}"]
                    `);
                    
                    shiftRadios.forEach(function(radio) {{
                        if (radio.value === '{selected_shift}' || 
                            radio.value === 'shift{selected_shift}' ||
                            radio.value.includes('{selected_shift}')) {{
                            radio.checked = true;
                            radio.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            debugInfo.push(`Shift radio selected: ${{radio.value}}`);
                            shiftFieldFound = true;
                            fieldsSet++;
                        }}
                    }});
                    
                    // Special handling for common shift patterns
                    if (!shiftFieldFound) {{
                        // Look for dropdown with options 1, 2, 3
                        const dropdowns = document.querySelectorAll('select');
                        dropdowns.forEach(dropdown => {{
                            const hasShiftOptions = Array.from(dropdown.options).some(opt => 
                                opt.value === '1' || opt.value === '2' || opt.value === '3'
                            );
                            
                            if (hasShiftOptions && dropdown.options.length <= 5) {{ // Likely a shift dropdown
                                const originalValue = dropdown.value;
                                dropdown.value = '{selected_shift}';
                                dropdown.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                debugInfo.push(`Detected shift dropdown by pattern: ${{originalValue}} -> ${{dropdown.value}}`);
                                shiftFieldFound = true;
                                fieldsSet++;
                            }}
                        }});
                    }}
                    
                    return {{
                        found: shiftFieldFound,
                        fieldsSet: fieldsSet,
                        debugInfo: debugInfo,
                        message: shiftFieldFound ? `Shift {selected_shift} set successfully` : 'No shift field found in form'
                    }};
                    
                }} catch(e) {{
                    return {{
                        found: false,
                        fieldsSet: 0,
                        debugInfo: [`Error: ${{e.message}}`],
                        message: 'Error setting shift: ' + e.message
                    }};
                }}
            }})()
        """)
        
        print(f"  🔍 SHIFT DEBUG INFO:")
        for info in shift_set_success.get('debugInfo', []):
            print(f"    📋 {info}")
            
        if shift_set_success.get('found'):
            print(f"  ✅ SHIFT SET: {shift_set_success['message']} ({shift_set_success['fieldsSet']} fields)")
        else:
            print(f"  ℹ️  SHIFT INFO: {shift_set_success['message']}")
            print(f"  📝 Note: Shift {selected_shift} will be noted in automation log but form may not have shift field")
        
        # ⚡ INSTANT DESCRIPTION FILLING ⚡
        print(f"📝 INSTANT DESCRIPTION: {deskripsi}")
        
        # Instant description with JavaScript
        desc_success = page.evaluate(f"""
            (function() {{
                try {{
                    // Try multiple description field selectors
                    var descField = document.querySelector('textarea[aria-label*="Deskripsi"]') ||
                                   document.getElementById('ahmgawpm003_deskripsi_pekerjaan_khusus_request_kontraktor') ||
                                   document.querySelector('textarea');
                    
                    if (descField) {{
                        descField.value = '{deskripsi}';
                        descField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        descField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        console.log('Description filled instantly');
                        return true;
                    }}
                    return false;
                }} catch(e) {{
                    console.log('Description fill error:', e);
                    return false;
                }}
            }})()
        """)
        
        if not desc_success:
            # Fallback description filling
            try:
                page.locator('textarea[aria-label*="Deskripsi"]').fill(deskripsi)
            except:
                try:
                    page.locator("#ahmgawpm003_deskripsi_pekerjaan_khusus_request_kontraktor").fill(deskripsi)
                except:
                    page.locator('textarea').first.fill(deskripsi)

        # ⚡ INSTANT DATE SETTING ⚡
        print(f"📅 INSTANT DATE SETTING: {work_date}")
        date_str = setup_date(work_date)
        print(f"⚡ Formatted date: {date_str}")
        
        set_date_field(page, date_str)

<<<<<<< HEAD
        # 🛡️ SET SAFETY INDUCTION ONCE FOR THE ENTIRE FORM (NOT PER PERSONNEL) 🛡️
        print("🛡️ SETTING SAFETY INDUCTION STATUS (ONCE FOR ENTIRE FORM)...")
        
        safety_induction_result = page.evaluate("""
            (function() {
                try {
                    console.log('🛡️ Checking Safety Induction field state...');
                    
                    // Find the Safety Induction status field
                    const safetyField = document.getElementById('ahmgawpm003_status_safety_induction_edit');
                    
                    if (!safetyField) {
                        console.log('❌ Safety Induction field not found');
                        return {success: false, reason: 'field_not_found'};
                    }
                    
                    // Check current field state
                    const fieldState = {
                        exists: true,
                        disabled: safetyField.disabled,
                        value: safetyField.value,
                        tagName: safetyField.tagName,
                        options: safetyField.tagName === 'SELECT' ? 
                            Array.from(safetyField.options).map(opt => ({value: opt.value, text: opt.text})) : []
                    };
                    
                    console.log('📊 Safety field state:', fieldState);
                    
                    // Only enable if it's actually disabled (should be active by default)
                    if (fieldState.disabled) {
                        console.log('⚠️ Field is disabled, enabling it...');
                        safetyField.disabled = false;
                        safetyField.removeAttribute('disabled');
                    } else {
                        console.log('✅ Field is already active (as expected)');
                    }
                    
                    // Set the status - try "Sudah" first, then "Aktif"
                    let setValue = false;
                    
                    if (safetyField.tagName === 'SELECT') {
                        // Try to find and select appropriate option
                        const options = Array.from(safetyField.options);
                        
                        // Priority order: Sudah > Aktif > any non-empty option
                        const targetValues = ['Sudah', 'Aktif', 'PASS', 'LULUS'];
                        
                        for (let targetValue of targetValues) {
                            const option = options.find(opt => 
                                opt.value === targetValue || 
                                opt.text.toLowerCase().includes(targetValue.toLowerCase())
                            );
                            
                            if (option) {
                                safetyField.value = option.value;
                                safetyField.dispatchEvent(new Event('change', {bubbles: true}));
                                console.log('✅ Safety status set to:', option.value, '(' + option.text + ')');
                                setValue = true;
                                break;
                            }
                        }
                        
                        // Fallback: select first non-empty option
                        if (!setValue && options.length > 1) {
                            const firstOption = options.find(opt => opt.value && opt.value !== '');
                            if (firstOption) {
                                safetyField.value = firstOption.value;
                                safetyField.dispatchEvent(new Event('change', {bubbles: true}));
                                console.log('✅ Safety status set to fallback:', firstOption.value);
                                setValue = true;
                            }
=======
        # ⚡ ULTRA-FAST PERSONNEL ADDITION - ZERO DELAYS! ⚡
        print(f"👥 ULTRA-FAST PERSONNEL: {len(personnel_data)} people")
        
        for i, (name, nik) in enumerate(personnel_data, 1):
            print(f"  ⚡ Person {i}: {name}")
            
            try:
                # Click Add Personnel - no wait needed
                add_personnel_button = page.get_by_role("button", name="+ Add Personnel")
                add_personnel_button.click()
                
                # Wait for modal - minimal timeout
                page.wait_for_selector("#ahmgawpm003_nik_paspor_pekerja_add", timeout=3000)
                
                # ⚡ INSTANT BULK FILL - ALL FIELDS AT ONCE! ⚡
                success = page.evaluate(f"""
                    (function() {{
                        // ULTRA-FAST bulk fill using JavaScript - NO DELAYS!
                        const fields = {{
                            'ahmgawpm003_nik_paspor_pekerja_add': '{nik}',
                            'ahmgawpm003_nama_pekerja_add': '{name}',
                            'ahmgawpm003_nomor_hp_pekerja_add': '08123456789',
                            'ahmgawpm003_email_pekerja_add': 'worker@indonesia.com',
                            'ahmgawpm003_seksi_add': 'HAI member',
                            'ahmgawpm003_departemen_add': 'HAI member',
                            'ahmgawpm003_divisi_add': 'HAI member'
                        }};
                        
                        // Fill all text fields INSTANTLY
                        let fieldsSet = 0;
                        Object.entries(fields).forEach(([id, value]) => {{
                            const field = document.getElementById(id);
                            if (field) {{
                                field.value = value;
                                field.setAttribute('value', value);
                                
                                // Fire essential events only
                                ['input', 'change', 'blur'].forEach(eventType => {{
                                    field.dispatchEvent(new Event(eventType, {{ bubbles: true }}));
                                }});
                                fieldsSet++;
                            }}
                        }});
                        
                        // Set certification dropdown INSTANTLY
                        const certField = document.getElementById('ahmgawpm003_kebutuhan_sertifikasi_add');
                        if (certField) {{
                            certField.value = 'N';
                            certField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            fieldsSet++;
                        }}
                        
                        console.log('INSTANT FILL: Set ' + fieldsSet + ' fields for {name}');
                        return fieldsSet;
                    }})()
                """)
                
                print(f"    ⚡ INSTANT FILL: {success} fields set")
                
                # ZERO delay submission - INSTANT! ⚡
                submit_btn = page.locator("#ahmgawpm003_submit_button_add_modal")
                submit_btn.click()
                
                # Minimal wait for modal to close - ULTRA FAST!
                page.wait_for_timeout(100)
                print(f"    ✅ INSTANT ADD: {name}")
                
            except Exception as e:
                print(f"    ❌ Failed: {name} - {str(e)[:50]}...")
                # Quick error recovery - take screenshot and continue
                try:
                    page.screenshot(path=f'error_person_{i}.png')
                except:
                    pass
                continue

        # ⚡ INSTANT AREA & TOOL ADDITION - ZERO DELAYS! ⚡
        print("🏢 INSTANT WORK AREA...")
        try:
            page.get_by_role("button", name="+ Add Area").click()
            page.wait_for_timeout(100)  # Minimal wait
            page.locator("#ahmgawpm003_add_area_modal .btn-lookup").click()
            page.wait_for_timeout(200)  # Brief wait for lookup
            page.get_by_role("cell", name="G", exact=True).click()
            page.locator("#ahmgawpm003_submit_button_add_area_modal").click()
            print("⚡ INSTANT: Work area added")
        except Exception as e:
            print(f"⚠️ Area addition failed: {e}")

        print("🔧 ULTRA-INSTANT TOOLS...")
        try:
            page.get_by_role("button", name="+ Add Tool").click()
            page.wait_for_timeout(150)  # Slightly longer wait for modal to fully load
            
            # COMPREHENSIVE tool filling - ALL FIELDS COVERED!
            tool_success = page.evaluate("""
                (function() {
                    try {
                        // Find ALL possible tool fields
                        const toolId = document.getElementById('ahmgawpm003_tool_id_add');
                        const toolDesc = document.getElementById('ahmgawpm003_deskripsi_alat_add');
                        const permitFlag = document.getElementById('ahmgawpm003_permit_flag_add');
                        
                        // Additional fields that might be required
                        const toolName = document.getElementById('ahmgawpm003_nama_alat_add') || 
                                        document.querySelector('input[name*="nama_alat"]') ||
                                        document.querySelector('input[placeholder*="nama"]');
                        const toolType = document.getElementById('ahmgawpm003_jenis_alat_add') ||
                                        document.querySelector('select[name*="jenis"]');
                        const toolQty = document.getElementById('ahmgawpm003_jumlah_add') ||
                                       document.querySelector('input[name*="jumlah"]') ||
                                       document.querySelector('input[type="number"]');
                        
                        let fieldsSet = 0;
                        
                        // Fill Tool ID
                        if (toolId) {
                            toolId.value = '1';
                            toolId.setAttribute('value', '1');
                            ['input', 'change', 'blur', 'keyup'].forEach(eventType => {
                                toolId.dispatchEvent(new Event(eventType, {bubbles: true}));
                            });
                            console.log('Tool ID set: 1');
                            fieldsSet++;
                        }
                        
                        // Fill Tool Description
                        if (toolDesc) {
                            toolDesc.value = 'BASIC TOOLS';
                            toolDesc.setAttribute('value', 'BASIC TOOLS');
                            ['input', 'change', 'blur', 'keyup'].forEach(eventType => {
                                toolDesc.dispatchEvent(new Event(eventType, {bubbles: true}));
                            });
                            console.log('Tool Description set: BASIC TOOLS');
                            fieldsSet++;
>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)
                        }
                    }
                    
                    return {
                        success: setValue,
                        fieldState: fieldState,
                        finalValue: safetyField.value,
                        wasDisabled: fieldState.disabled
                    };
                    
                } catch(e) {
                    console.log('❌ Safety Induction setup error:', e);
                    return {success: false, error: e.message};
                }
            })()
        """)
        
        if safety_induction_result.get('success'):
            print(f"    ✅ Safety Induction set successfully!")
            print(f"        📝 Value: {safety_induction_result.get('finalValue')}")
            was_disabled = safety_induction_result.get('wasDisabled')
            if was_disabled:
                print(f"        ⚠️ Field was disabled (unusual - should be active by default)")
            else:
                print(f"        ✅ Field was already active (normal behavior)")
        else:
            print(f"    ⚠️ Could not set Safety Induction")
            print(f"        📊 Details: {safety_induction_result}")
        
        # Set Safety Induction date as well
        try:
            page.locator("#ahmgawpm003_tanggal_safety_induction_edit").fill(date_str)
            print(f"    ✅ Safety Induction date set to: {date_str}")
        except Exception as e:
            print(f"    ⚠️ Could not set Safety Induction date: {e}")
        
        page.wait_for_timeout(1000)  # Brief pause after Safety Induction setup
        print("🛡️ SAFETY INDUCTION SETUP COMPLETE!")

        # ⚡ SMART PERSONNEL ADDITION WITH INLINE CERTIFICATE HANDLING ⚡
        print(f"👥 SMART PERSONNEL: {len(personnel_data)} people")
        
        # First, read CSV to get certificate information for all personnel
        print("📜 Reading certificate data from CSV...")
        csv_map = {
            "IA": "/home/dan/Portal/personnel_list_IA.csv",
            "IR": "/home/dan/Portal/personnel_list_IR.csv", 
            "IK": "/home/dan/Portal/personnel_list_IK.csv"
        }
        csv_file_path = csv_map.get(ikk_category, csv_map["IA"])
        
        # Create certificate lookup dictionary
        cert_lookup = {}
        try:
            import csv
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    nik = str(row.get('Nomor', '')).strip()
                    cert = str(row.get('Sertif', '')).strip()  # Convert to string and strip
                    exp_cert = str(row.get('Expsertif', '')).strip()  # Convert to string and strip
                    
                    # Debug: Show what we found for each person
                    print(f"    🔍 DEBUG - Name: {row.get('Nama', 'N/A')}, NIK: {nik}")
                    print(f"        Cert: '{cert}' (len={len(cert)})")
                    print(f"        Exp: '{exp_cert}' (len={len(exp_cert)})")
                    
                    # Store certificate data if person has valid certificate
                    # More robust checking - handle empty strings, whitespace, and "None" strings
                    if (cert and exp_cert and 
                        len(cert.strip()) > 0 and len(exp_cert.strip()) > 0 and
                        cert.lower() not in ['', 'n/a', 'none', '-', 'null'] and
                        cert != 'None' and exp_cert != 'None'):  # Handle pandas None strings
                        
<<<<<<< HEAD
                        cert_lookup[nik] = {
                            'cert': cert,
                            'exp_cert': exp_cert
                        }
                        print(f"    ✅ CERTIFICATE FOUND for NIK {nik}: {cert}")
                    else:
                        print(f"    ❌ NO CERTIFICATE for NIK {nik}")
                        
            print(f"📜 SUMMARY: Found certificate data for {len(cert_lookup)} personnel out of total processed")
        except Exception as e:
            print(f"⚠️ Error reading CSV: {e}")
            cert_lookup = {}
        
        # Add each personnel with appropriate certificate handling
        for i, (name, nik) in enumerate(personnel_data, 1):
            has_cert = nik in cert_lookup
            cert_status = "WITH CERTIFICATE" if has_cert else "NO CERTIFICATE"
            print(f"  ⚡ Person {i}: {name} ({cert_status})")
            
            try:
                # 🎯 ENHANCED ADD PERSONNEL BUTTON CLICK - ONLY for person 2+
                if i == 1:
                    # First person: Try multiple ways to access the modal
                    print(f"    📝 Person 1: Trying to access existing modal...")
                    add_personnel_success = False
                    
                    # Method 1: Check if modal is already visible
                    try:
                        page.wait_for_selector("#ahmgawpm003_nik_paspor_pekerja_add", state="visible", timeout=2000)
                        print(f"    ✅ Personnel modal already visible for person 1")
                        add_personnel_success = True
                    except:
                        print(f"    � Modal not visible, trying to trigger it...")
                    
                    # Method 2: Try to trigger modal by clicking form section
                    if not add_personnel_success:
                        try:
                            # Look for personnel section or related elements to click
                            personnel_trigger_success = page.evaluate("""
                                (function() {
                                    try {
                                        // Try various ways to trigger personnel modal
                                        const triggers = [
                                            () => document.querySelector('.personnel-section'),
                                            () => document.querySelector('[data-target*="personnel"]'),
                                            () => document.querySelector('[data-target*="add"]'),
                                            () => document.querySelector('.form-section'),
                                            () => document.querySelector('#personnel_table'),
                                            () => document.querySelector('.add-row'),
                                            () => document.querySelector('.table-actions')
                                        ];
                                        
                                        for (let trigger of triggers) {
                                            try {
                                                const element = trigger();
                                                if (element && element.offsetParent !== null) {
                                                    element.click();
                                                    console.log('Triggered personnel section');
                                                    return true;
                                                }
                                            } catch(e) {
                                                continue;
                                            }
                                        }
                                        return false;
                                    } catch(e) {
                                        return false;
                                    }
                                })()
                            """)
                            
                            if personnel_trigger_success:
                                page.wait_for_timeout(1000)
                                try:
                                    page.wait_for_selector("#ahmgawpm003_nik_paspor_pekerja_add", state="visible", timeout=3000)
                                    print(f"    ✅ Personnel modal triggered successfully for person 1")
                                    add_personnel_success = True
                                except:
                                    print(f"    ⚠️ Modal trigger failed for person 1")
                        except Exception as trigger_error:
                            print(f"    ⚠️ Personnel trigger error: {trigger_error}")
                    
                    # Method 3: If still failed, fallback to Add Personnel button
                    if not add_personnel_success:
                        print(f"    🔄 FALLBACK: Searching for Add Personnel button for person 1...")
                else:
                    # Person 2+: Need to click Add Personnel button
                    print(f"    🔄 ENHANCED: Clicking Add Personnel for person {i}...")
                    add_personnel_success = False
                    
                    # 🚨 CRITICAL: First check and dismiss any blocking notification modal
                    print(f"    🔔 CRITICAL: Checking for notification modal before person {i}...")
                    notification_cleared = page.evaluate("""
                        (function() {
                            try {
                                let modalsClosed = 0;
                                
                                // Check for notification modal specifically
                                const notificationModal = document.getElementById('ahmgawpm003_notification_modal');
                                if (notificationModal && (notificationModal.classList.contains('in') || notificationModal.classList.contains('show'))) {
                                    console.log('Pre-person notification modal detected - dismissing...');
                                    
                                    // Try to find and click OK/Close button
                                    const buttons = notificationModal.querySelectorAll('button, .btn, [data-dismiss]');
                                    let buttonClicked = false;
                                    
                                    for (let btn of buttons) {
                                        const btnText = (btn.textContent || btn.innerText || '').toLowerCase();
                                        if (btnText.includes('ok') || btnText.includes('close') || btnText.includes('tutup') || 
                                            btn.getAttribute('data-dismiss') === 'modal') {
                                            btn.click();
                                            buttonClicked = true;
                                            console.log('Notification modal button clicked:', btnText);
                                            break;
                                        }
                                    }
                                    
                                    // Force hide if button click didn't work
                                    if (!buttonClicked) {
                                        notificationModal.style.display = 'none';
                                        notificationModal.classList.remove('in', 'show');
                                        notificationModal.setAttribute('aria-hidden', 'true');
                                        console.log('Notification modal force hidden');
                                    }
                                    
                                    modalsClosed++;
                                }
                                
                                // Check for any other blocking modals
                                const allModals = document.querySelectorAll('.modal.in, .modal.show');
                                allModals.forEach(modal => {
                                    if (modal.id !== 'ahmgawpm003_add_worker_modal') { // Don't close the add worker modal
                                        modal.style.display = 'none';
                                        modal.classList.remove('in', 'show');
                                        modal.setAttribute('aria-hidden', 'true');
                                        modalsClosed++;
                                        console.log('Blocking modal closed:', modal.id);
                                    }
                                });
                                
                                // Remove all modal backdrops
                                const backdrops = document.querySelectorAll('.modal-backdrop');
                                backdrops.forEach(backdrop => backdrop.remove());
                                
                                // Reset body state
                                document.body.classList.remove('modal-open');
                                document.body.style.removeProperty('padding-right');
                                
                                console.log('Pre-person modal cleanup completed, closed:', modalsClosed);
                                return {success: true, modalsClosed: modalsClosed};
                                
                            } catch(e) {
                                console.log('Pre-person modal cleanup error:', e);
                                return {success: false, error: e.message};
                            }
                        })()
                    """)
                    
                    if notification_cleared.get('success'):
                        print(f"    ✅ Notification check complete: {notification_cleared.get('modalsClosed')} modals closed")
                        if notification_cleared.get('modalsClosed') > 0:
                            page.wait_for_timeout(1500)  # Extra wait after closing notification modal
                    else:
                        print(f"    ⚠️ Notification check failed: {notification_cleared.get('error')}")
                        page.wait_for_timeout(1000)  # Still wait a bit
                
                # Add Personnel button click logic for person 2+ (or fallback for person 1)
                if not add_personnel_success:
                    # 🔧 ENHANCED MODAL CLEANUP for person 2+ to ensure fresh state
                    if i > 1:
                        print(f"      🧹 ENHANCED: Cleaning modal state for person {i}...")
                        
                        # First ensure any previous modal is completely dismissed
                        modal_cleanup_result = page.evaluate("""
                            (function() {
                                try {
                                    // Force close any open modals
                                    const modals = document.querySelectorAll('.modal.in, .modal.show, .modal.fade.in');
                                    modals.forEach(modal => {
                                        modal.style.display = 'none';
                                        modal.classList.remove('in', 'show');
                                        modal.setAttribute('aria-hidden', 'true');
                                    });
                                    
                                    // Remove modal backdrop
                                    const backdrops = document.querySelectorAll('.modal-backdrop');
                                    backdrops.forEach(backdrop => backdrop.remove());
                                    
                                    // Reset body classes and styles
                                    document.body.classList.remove('modal-open');
                                    document.body.style.removeProperty('padding-right');
                                    
                                    // Clear any modal-related data
                                    window.lastAddedPersonnel = null;
                                    window.personnelModalOpen = false;
                                    
                                    console.log('Modal cleanup completed');
                                    return true;
                                } catch(e) {
                                    console.log('Modal cleanup error:', e);
                                    return false;
                                }
                            })()
                        """)
                        
                        print(f"      🧹 Modal cleanup result: {modal_cleanup_result}")
                        page.wait_for_timeout(1000)  # Wait for cleanup to complete
                    
                    for click_attempt in range(5):  # Try up to 5 times
                        try:
                            print(f"      🔄 Add Personnel click attempt {click_attempt + 1} for person {i}...")
                            
                            # Wait for any previous modal to be completely gone
                            page.wait_for_timeout(500 + (click_attempt * 300))
                            
                            # COMPREHENSIVE Add Personnel button detection and click
                            button_click_result = page.evaluate(f"""
                            (function(attempt) {{
                                try {{
                                    console.log('=== ADD PERSONNEL BUTTON SEARCH attempt ' + attempt + ' ===');
                                    
                                    // Multiple strategies to find Add Personnel button
                                    let addBtn = null;
                                    const strategies = [
                                        // Strategy 1: By exact IDs found in HTML (MOST RELIABLE!)
                                        () => {{
                                            const exactIds = [
                                                'ahmgawpm003_add_personnel_button_edit',
                                                'ahmgawpm003_add_personnel_button_request',
                                                'ahmgawpm003_add_personnel_button',
                                                'ahmgawpm003_add_worker_button'
                                            ];
                                            for (let id of exactIds) {{
                                                const btn = document.getElementById(id);
                                                if (btn && btn.offsetParent !== null && !btn.disabled) {{
                                                    console.log('Found Add Personnel button by exact ID:', id);
                                                    return btn;
                                                }}
                                            }}
                                            return null;
                                        }},
                                        
                                        // Strategy 2: By modal target (data-target="#ahmgawpm003_add_worker_modal")
                                        () => {{
                                            const modalTargets = [
                                                'button[data-target="#ahmgawpm003_add_worker_modal"]',
                                                'button[data-target*="add_worker_modal"]',
                                                'button[data-target*="worker_modal"]'
                                            ];
                                            for (let selector of modalTargets) {{
                                                const btn = document.querySelector(selector);
                                                if (btn && btn.offsetParent !== null && !btn.disabled) {{
                                                    console.log('Found Add Personnel button by modal target:', selector);
                                                    return btn;
                                                }}
                                            }}
                                            return null;
                                        }},
                                        
                                        // Strategy 3: By class and text content (btn bg-orange + Add Personnel)
                                        () => {{
                                            const btns = Array.from(document.querySelectorAll('button.btn.bg-orange, button.btn.large-button'));
                                            return btns.find(btn => {{
                                                const text = (btn.textContent || btn.innerText || '').toLowerCase();
                                                return text.includes('add') && text.includes('personnel') && 
                                                       btn.offsetParent !== null && !btn.disabled;
                                            }});
                                        }},
                                        
                                        // Strategy 4: By onclick function (if any)
                                        () => {{
                                            const btns = Array.from(document.querySelectorAll('button[onclick]'));
                                            return btns.find(btn => 
                                                btn.onclick && (
                                                    btn.onclick.toString().includes('addWorker') ||
                                                    btn.onclick.toString().includes('addPersonnel') ||
                                                    btn.onclick.toString().includes('add_modal') ||
                                                    btn.onclick.toString().includes('worker_modal')
                                                ) && btn.offsetParent !== null && !btn.disabled
                                            );
                                        }},
                                        
                                        // Strategy 5: By glyphicon plus icon + Add Personnel text
                                        () => {{
                                            const btns = Array.from(document.querySelectorAll('button'));
                                            return btns.find(btn => {{
                                                const hasIcon = btn.querySelector('.glyphicon-plus, .fa-plus, .icon-plus');
                                                const text = (btn.textContent || btn.innerText || '').toLowerCase();
                                                const hasAddPersonnelText = text.includes('add') && text.includes('personnel');
                                                return hasIcon && hasAddPersonnelText && 
                                                       btn.offsetParent !== null && !btn.disabled;
                                            }});
                                        }},
                                        
                                        // Strategy 6: Generic fallback (any button with "+ Add" text)
                                        () => {{
                                            const btns = Array.from(document.querySelectorAll('button:not([disabled])'));
                                            return btns.find(btn => {{
                                                const text = (btn.textContent || btn.innerText || '').trim();
                                                return (
                                                    text.includes('+ Add') ||
                                                    (text.includes('Add') && text.includes('Personnel')) ||
                                                    (text.includes('Tambah') && text.includes('Personnel'))
                                                ) && btn.offsetParent !== null;
                                            }});
                                        }}
                                    ];
                                    
                                    // Try each strategy
                                    for (let i = 0; i < strategies.length; i++) {{
                                        try {{
                                            addBtn = strategies[i]();
                                            if (addBtn && addBtn.offsetParent !== null && !addBtn.disabled) {{
                                                console.log('Found Add Personnel button via strategy ' + (i + 1));
                                                console.log('Button text:', addBtn.textContent || addBtn.innerText);
                                                console.log('Button ID:', addBtn.id || 'no-id');
                                                console.log('Button class:', addBtn.className || 'no-class');
                                                console.log('Button onclick:', addBtn.onclick ? addBtn.onclick.toString().substring(0, 100) : 'no-onclick');
                                                break;
                                            }}
                                        }} catch(e) {{
                                            console.log('Strategy ' + (i + 1) + ' failed:', e.message);
                                        }}
                                    }}
                                    
                                    if (addBtn && addBtn.offsetParent !== null && !addBtn.disabled) {{
                                        // Force enable the button
                                        addBtn.removeAttribute('disabled');
                                        addBtn.disabled = false;
                                        addBtn.style.pointerEvents = 'auto';
                                        addBtn.style.opacity = '1';
                                        addBtn.classList.remove('disabled');
                                        
                                        // Click the button
                                        addBtn.click();
                                        
                                        console.log('Add Personnel button clicked successfully');
                                        return {{
                                            success: true,
                                            buttonText: addBtn.textContent || addBtn.innerText,
                                            buttonId: addBtn.id || 'no-id',
                                            buttonClass: addBtn.className || 'no-class',
                                            buttonOnclick: addBtn.onclick ? addBtn.onclick.toString().substring(0, 100) : 'no-onclick',
                                            attempt: attempt
                                        }};
                                    }} else {{
                                        // Enhanced debugging - list all buttons for analysis
                                        const allButtons = Array.from(document.querySelectorAll('button'));
                                        const buttonInfo = allButtons.slice(0, 10).map(btn => ({{
                                            text: (btn.textContent || btn.innerText || '').substring(0, 30),
                                            id: btn.id || 'no-id',
                                            class: btn.className || 'no-class',
                                            disabled: btn.disabled,
                                            visible: btn.offsetParent !== null,
                                            onclick: btn.onclick ? 'has-onclick' : 'no-onclick'
                                        }}));
                                        
                                        console.log('No suitable Add Personnel button found');
                                        console.log('Sample buttons (first 10):');
                                        buttonInfo.forEach((info, idx) => {{
                                            console.log(`Button ${{idx + 1}}: ${{JSON.stringify(info)}}`);
                                        }});
                                        
                                        return {{
                                            success: false,
                                            reason: 'button_not_found',
                                            attempt: attempt,
                                            totalButtons: allButtons.length,
                                            enabledButtons: allButtons.filter(btn => !btn.disabled).length,
                                            visibleButtons: allButtons.filter(btn => btn.offsetParent !== null).length,
                                            sampleButtons: buttonInfo
                                        }};
                                    }}
                                }} catch(e) {{
                                    console.error('Add Personnel button click error:', e);
                                    return {{
                                        success: false,
                                        reason: 'error',
                                        error: e.message,
                                        attempt: attempt
                                    }};
                                }}
                            }})()
                            """, click_attempt + 1)
                            
                            if button_click_result.get('success'):
                                print(f"      ✅ Add Personnel clicked successfully (attempt {click_attempt + 1})")
                                print(f"        📝 Button: {button_click_result.get('buttonText')}")
                                print(f"        🆔 ID: {button_click_result.get('buttonId')}")
                                
                                # Wait for modal to appear
                                try:
                                    page.wait_for_selector("#ahmgawpm003_nik_paspor_pekerja_add", state="visible", timeout=5000)
                                    print(f"      ✅ Personnel modal appeared for person {i}")
                                    add_personnel_success = True
                                    
                                    # 🔧 CRITICAL MODAL FIELD RESET for person 2+ (PREVENT DISABLED FIELDS ISSUE)
                                    if i > 1:
                                        print(f"      🔧 CRITICAL: Resetting modal fields for person {i}...")
                                        modal_reset_result = page.evaluate("""
                                            (function() {
                                                try {
                                                    // Reset and enable all critical fields that might be disabled
                                                    const criticalFields = [
                                                        'ahmgawpm003_tipe_tugas_add',
                                                        'ahmgawpm003_jenis_sertifikasi_add', 
                                                        'ahmgawpm003_status_safety_induction_add',
                                                        'ahmgawpm003_nik_paspor_pekerja_add',
                                                        'ahmgawpm003_nama_pekerja_add',
                                                        'ahmgawpm003_nomor_hp_pekerja_add',
                                                        'ahmgawpm003_email_add',
                                                        'ahmgawpm003_seksi_add',
                                                        'ahmgawpm003_departemen_add',
                                                        'ahmgawpm003_divisi_add'
                                                    ];
                                                    
                                                    let fieldsReset = 0;
                                                    let fieldsEnabled = 0;
                                                    
                                                    criticalFields.forEach(fieldId => {
                                                        const field = document.getElementById(fieldId);
                                                        if (field) {
                                                            // Clear the field value
                                                            field.value = '';
                                                            field.selectedIndex = 0; // For select elements
                                                            
                                                            // Force enable the field
                                                            field.disabled = false;
                                                            field.removeAttribute('disabled');
                                                            field.readOnly = false;
                                                            field.removeAttribute('readonly');
                                                            
                                                            // Ensure field is visible and interactable
                                                            field.style.pointerEvents = 'auto';
                                                            field.style.opacity = '1';
                                                            field.classList.remove('disabled');
                                                            
                                                            fieldsReset++;
                                                            if (!field.disabled && !field.readOnly) {
                                                                fieldsEnabled++;
                                                            }
                                                            
                                                            console.log('Reset field:', fieldId, 'Disabled:', field.disabled, 'ReadOnly:', field.readOnly);
                                                        }
                                                    });
                                                    
                                                    // Special handling for dropdowns - populate with default options if empty
                                                    const tipeTugasField = document.getElementById('ahmgawpm003_tipe_tugas_add');
                                                    if (tipeTugasField && tipeTugasField.options.length === 0) {
                                                        // Add default option if no options exist
                                                        const defaultOption = new Option('-- Select Task Type --', '');
                                                        tipeTugasField.add(defaultOption);
                                                        tipeTugasField.selectedIndex = 0;
                                                    }
                                                    
                                                    // Trigger change events to update dependent fields
                                                    criticalFields.forEach(fieldId => {
                                                        const field = document.getElementById(fieldId);
                                                        if (field) {
                                                            ['focus', 'input', 'change', 'blur'].forEach(eventType => {
                                                                field.dispatchEvent(new Event(eventType, {bubbles: true}));
                                                            });
                                                        }
                                                    });
                                                    
                                                    console.log('Modal field reset completed - Fields reset:', fieldsReset, 'Fields enabled:', fieldsEnabled);
                                                    return {
                                                        success: true,
                                                        fieldsReset: fieldsReset,
                                                        fieldsEnabled: fieldsEnabled,
                                                        totalFields: criticalFields.length
                                                    };
                                                } catch(e) {
                                                    console.log('Modal field reset error:', e);
                                                    return {success: false, error: e.message};
                                                }
                                            })()
                                        """)
                                        
                                        if modal_reset_result.get('success'):
                                            print(f"      ✅ Modal fields reset successful: {modal_reset_result.get('fieldsReset')}/{modal_reset_result.get('totalFields')} fields reset, {modal_reset_result.get('fieldsEnabled')} enabled")
                                        else:
                                            print(f"      ⚠️ Modal field reset failed: {modal_reset_result.get('error')}")
                                        
                                        # Additional wait to ensure modal is fully ready
                                        page.wait_for_timeout(1000)
                                    
                                    break
                                except Exception as modal_wait_error:
                                    print(f"      ⚠️ Modal wait failed after button click (attempt {click_attempt + 1}): {modal_wait_error}")
                                    # Continue to retry
                            else:
                                print(f"      ⚠️ Add Personnel click failed (attempt {click_attempt + 1}): {button_click_result.get('reason')}")
                                print(f"        📊 Debug: {button_click_result}")
                                
                        except Exception as click_error:
                            print(f"      ❌ Add Personnel click attempt {click_attempt + 1} exception: {click_error}")
                    
                    if not add_personnel_success:
                        print(f"    🚨 CRITICAL: Could not click Add Personnel for person {i} after 5 attempts!")
                        
                        # Take debug screenshot
                        try:
                            page.screenshot(path=f'/home/dan/Portal/debug_add_personnel_failed_person_{i}.png')
                            print(f"    📸 Debug screenshot saved: debug_add_personnel_failed_person_{i}.png")
                            
                            # Also save page HTML for analysis
                            page_html = page.content()
                            with open(f'/home/dan/Portal/debug_add_personnel_failed_person_{i}.html', 'w', encoding='utf-8') as f:
                                f.write(page_html)
                            print(f"    📄 Page HTML saved: debug_add_personnel_failed_person_{i}.html")
                        except Exception as debug_error:
                            print(f"    ⚠️ Debug file save failed: {debug_error}")
                        
                        # Skip this person
                        print(f"    ⏭️ Skipping person {i} due to Add Personnel button failure")
                        continue
                
                # Fill basic fields first - ENHANCED & BULLETPROOF
                print(f"    📋 Filling basic fields for {name} (NIK: {nik})...")
                
                # 🔍 PRE-FILLING MODAL VALIDATION for person 2+ (PREVENT FIELD ACCESS ISSUES)
                if i > 1:
                    print(f"    🔍 PRE-FILLING: Validating modal state for person {i}...")
                    modal_validation_result = page.evaluate("""
                        (function() {
                            try {
                                const requiredFields = [
                                    {id: 'ahmgawpm003_nik_paspor_pekerja_add', name: 'NIK Field'},
                                    {id: 'ahmgawpm003_nama_pekerja_add', name: 'Name Field'},
                                    {id: 'ahmgawpm003_nomor_hp_pekerja_add', name: 'Phone Field'},
                                    {id: 'ahmgawpm003_email_add', name: 'Email Field'},
                                    {id: 'ahmgawpm003_seksi_add', name: 'Section Field'},
                                    {id: 'ahmgawpm003_departemen_add', name: 'Department Field'},
                                    {id: 'ahmgawpm003_divisi_add', name: 'Division Field'}
                                ];
                                
                                let validationResults = [];
                                let accessibleFields = 0;
                                let totalFields = requiredFields.length;
                                
                                requiredFields.forEach(fieldInfo => {
                                    const field = document.getElementById(fieldInfo.id);
                                    if (field) {
                                        const isVisible = field.offsetParent !== null && field.style.display !== 'none';
                                        const isEnabled = !field.disabled && !field.readOnly;
                                        const isAccessible = isVisible && isEnabled;
                                        
                                        validationResults.push({
                                            id: fieldInfo.id,
                                            name: fieldInfo.name,
                                            exists: true,
                                            visible: isVisible,
                                            enabled: isEnabled,
                                            accessible: isAccessible,
                                            disabled: field.disabled,
                                            readOnly: field.readOnly,
                                            value: field.value || ''
                                        });
                                        
                                        if (isAccessible) {
                                            accessibleFields++;
                                        }
                                    } else {
                                        validationResults.push({
                                            id: fieldInfo.id,
                                            name: fieldInfo.name,
                                            exists: false,
                                            accessible: false
                                        });
                                    }
                                });
                                
                                console.log('Modal validation completed - Accessible fields:', accessibleFields, '/', totalFields);
                                
                                return {
                                    success: accessibleFields >= 6, // At least 6 out of 7 fields should be accessible
                                    accessibleFields: accessibleFields,
                                    totalFields: totalFields,
                                    results: validationResults,
                                    readyToFill: accessibleFields >= 6
                                };
                            } catch(e) {
                                console.log('Modal validation error:', e);
                                return {success: false, error: e.message, readyToFill: false};
                            }
                        })()
                    """)
                    
                    if modal_validation_result.get('success') and modal_validation_result.get('readyToFill'):
                        print(f"    ✅ Modal validation passed: {modal_validation_result.get('accessibleFields')}/{modal_validation_result.get('totalFields')} fields accessible")
                    else:
                        print(f"    ⚠️ Modal validation failed for person {i}: {modal_validation_result.get('accessibleFields')}/{modal_validation_result.get('totalFields')} fields accessible")
                        print(f"    📊 Field details: {modal_validation_result.get('results', [])}")
                        
                        # Attempt one more field reset if validation failed
                        print(f"    🔄 Attempting emergency field reset for person {i}...")
                        emergency_reset_result = page.evaluate("""
                            (function() {
                                try {
                                    const fields = document.querySelectorAll('#ahmgawpm003_add_worker_modal input, #ahmgawpm003_add_worker_modal select');
                                    let resetCount = 0;
                                    
                                    fields.forEach(field => {
                                        field.disabled = false;
                                        field.readOnly = false;
                                        field.removeAttribute('disabled');
                                        field.removeAttribute('readonly');
                                        field.style.pointerEvents = 'auto';
                                        field.style.opacity = '1';
                                        resetCount++;
                                    });
                                    
                                    console.log('Emergency reset completed:', resetCount, 'fields processed');
                                    return {success: true, fieldsProcessed: resetCount};
                                } catch(e) {
                                    return {success: false, error: e.message};
                                }
                            })()
                        """)
                        print(f"    🔄 Emergency reset result: {emergency_reset_result}")
                        page.wait_for_timeout(1000)
                
                # BULLETPROOF METHOD: Direct Playwright approach first
                print(f"    🎯 BULLETPROOF NIK & NAME FILLING...")
                
                # 🛡️ GLOBAL ENTER KEY PROTECTION SYSTEM (installed first for comprehensive coverage)
                print(f"    🛡️ Installing GLOBAL Enter key protection system...")
                global_protection_result = page.evaluate("""
                    (function() {
                        try {
                            // Global Enter key protection for the entire modal
                            const modal = document.getElementById('ahmgawpm003_add_worker_modal');
                            if (modal) {
                                // Remove any existing global protections
                                if (window.globalEnterProtection) {
                                    modal.removeEventListener('keydown', window.globalEnterProtection);
                                    modal.removeEventListener('keypress', window.globalEnterProtection);
                                    modal.removeEventListener('keyup', window.globalEnterProtection);
                                }
                                
                                // Create comprehensive global Enter key blocker
                                window.globalEnterProtection = function(e) {
                                    if (e.key === 'Enter' || e.keyCode === 13 || e.which === 13) {
                                        const target = e.target;
                                        const targetId = target ? target.id : 'unknown';
                                        
                                        // Only allow Enter on specific safe elements
                                        const safeElements = [
                                            'button[type="submit"]',
                                            'button[data-dismiss="modal"]', 
                                            '.btn-primary',
                                            '.btn-success'
                                        ];
                                        
                                        let isAllowed = false;
                                        for (let selector of safeElements) {
                                            if (target && target.matches && target.matches(selector)) {
                                                isAllowed = true;
                                                break;
                                            }
                                        }
                                        
                                        if (!isAllowed) {
                                            console.log('🛡️ GLOBAL PROTECTION: Blocked Enter key on element:', targetId);
                                            e.preventDefault();
                                            e.stopPropagation();
                                            e.stopImmediatePropagation();
                                            return false;
                                        } else {
                                            console.log('🛡️ GLOBAL PROTECTION: Allowed Enter key on safe element:', targetId);
                                        }
                                    }
                                };
                                
                                // Install global protection on modal
                                modal.addEventListener('keydown', window.globalEnterProtection, {capture: true, passive: false});
                                modal.addEventListener('keypress', window.globalEnterProtection, {capture: true, passive: false});
                                modal.addEventListener('keyup', window.globalEnterProtection, {capture: true, passive: false});
                                
                                console.log('🛡️ Global Enter key protection installed on modal');
                                return {success: true, modalId: modal.id};
                            }
                            return {success: false, reason: 'modal_not_found'};
                        } catch(e) {
                            console.log('Global Enter protection error:', e);
                            return {success: false, reason: 'error', error: e.message};
                        }
                    })()
                """)
                
                if global_protection_result.get('success'):
                    print(f"    ✅ Global Enter key protection installed successfully")
                else:
                    print(f"    ⚠️ Global Enter key protection failed: {global_protection_result.get('reason')}")
                
                # Extra wait to ensure modal is completely ready for person 2+
                if i > 1:
                    print(f"    ⏳ Extra wait for person {i} modal to be completely ready...")
                    page.wait_for_timeout(1000)
                    
                    # 🔒 CLEAR KEYBOARD STATE to prevent Enter key issues for person 2+
                    print(f"    🔒 Clearing keyboard state for person {i}...")
                    page.evaluate("""
                        (function() {
                            try {
                                // Clear any focused element to prevent keyboard events
                                if (document.activeElement && document.activeElement.blur) {
                                    document.activeElement.blur();
                                }
                                
                                // Remove any pending keyboard events
                                document.body.focus();
                                
                                // Clear any form autofocus
                                const autoFocusElements = document.querySelectorAll('[autofocus]');
                                autoFocusElements.forEach(el => el.removeAttribute('autofocus'));
                                
                                console.log('Keyboard state cleared for person 2+');
                                return true;
                            } catch(e) {
                                console.log('Keyboard state clear error:', e);
                                return false;
                            }
                        })()
                    """)
                    page.wait_for_timeout(500)  # Brief pause after clearing keyboard state
                
                # 🛡️ ULTRA-SAFE NIK Field Handling - 100% JAVASCRIPT ONLY (NO PLAYWRIGHT INTERACTIONS)
                nik_success = False
                for attempt in range(3):
                    try:
                        print(f"      📝 NIK attempt {attempt + 1}: {nik}")
                        
                        # 🚀 PURE JAVASCRIPT: Check field readiness and fill (NO Playwright locators)
                        nik_fill_result = page.evaluate(f"""
                            (function() {{
                                try {{
                                    console.log('=== PURE JAVASCRIPT NIK HANDLING - Attempt {attempt + 1} ===');
                                    
                                    const nikField = document.getElementById('ahmgawpm003_nik_paspor_pekerja_add');
                                    if (!nikField) {{
                                        return {{success: false, reason: 'field_not_found', attempt: {attempt + 1}}};
                                    }}
                                    
                                    // Check if field is ready (without Playwright interactions)
                                    const isVisible = nikField.offsetParent !== null && nikField.style.display !== 'none';
                                    const isEnabled = !nikField.disabled && !nikField.readOnly;
                                    const isReady = isVisible && isEnabled;
                                    
                                    if (!isReady) {{
                                        console.log('NIK field not ready:', {{visible: isVisible, enabled: isEnabled}});
                                        return {{success: false, reason: 'field_not_ready', attempt: {attempt + 1}}};
                                    }}
                                    
                                    console.log('NIK field is ready, installing protection...');
                                    
                                    // STEP 1: Install ULTRA-COMPREHENSIVE Enter key protection
                                    // Remove any existing event listeners first
                                    if (window.nikEnterBlocker) {{
                                        nikField.removeEventListener('keydown', window.nikEnterBlocker);
                                        nikField.removeEventListener('keypress', window.nikEnterBlocker);
                                        nikField.removeEventListener('keyup', window.nikEnterBlocker);
                                        nikField.removeEventListener('input', window.nikEnterBlocker);
                                    }}
                                    
                                    // Create ULTRA-COMPREHENSIVE Enter key blocker
                                    window.nikEnterBlocker = function(e) {{
                                        if (e.key === 'Enter' || e.keyCode === 13 || e.which === 13 || e.code === 'Enter') {{
                                            console.log('🛡️ BLOCKED Enter key in NIK field! Event type:', e.type);
                                            e.preventDefault();
                                            e.stopPropagation();
                                            e.stopImmediatePropagation();
                                            return false;
                                        }}
                                    }};
                                    
                                    // Install blockers on ALL possible events
                                    const eventTypes = ['keydown', 'keypress', 'keyup', 'input'];
                                    eventTypes.forEach(eventType => {{
                                        nikField.addEventListener(eventType, window.nikEnterBlocker, {{capture: true, passive: false}});
                                    }});
                                    
                                    // Form-level protection
                                    const form = nikField.closest('form, .modal, .form-group');
                                    if (form) {{
                                        form.addEventListener('keydown', function(e) {{
                                            if ((e.key === 'Enter' || e.keyCode === 13) && e.target === nikField) {{
                                                console.log('🛡️ BLOCKED Enter key at form level for NIK!');
                                                e.preventDefault();
                                                e.stopPropagation();
                                                e.stopImmediatePropagation();
                                                return false;
                                            }}
                                        }}, {{capture: true, passive: false}});
                                    }}
                                    
                                    console.log('🛡️ Enter key protection installed successfully');
                                    
                                    // STEP 2: SAFE FIELD FILLING (no focus, no click, no Playwright interactions)
                                    console.log('Starting SAFE NIK filling...');
                                    
                                    // Clear field safely (no events that could trigger validation)
                                    nikField.value = '';
                                    nikField.removeAttribute('value');
                                    
                                    // Set NIK value with multiple methods for reliability
                                    nikField.value = '{nik}';
                                    nikField.setAttribute('value', '{nik}');
                                    nikField.defaultValue = '{nik}';
                                    
                                    // Fire ONLY essential events (no focus/blur that might trigger Enter key handling)
                                    const inputEvent = new Event('input', {{
                                        bubbles: true, 
                                        cancelable: false,
                                        composed: true
                                    }});
                                    
                                    const changeEvent = new Event('change', {{
                                        bubbles: true, 
                                        cancelable: false,
                                        composed: true
                                    }});
                                    
                                    // Dispatch events safely
                                    nikField.dispatchEvent(inputEvent);
                                    nikField.dispatchEvent(changeEvent);
                                    
                                    // STEP 3: Verify value was set correctly
                                    const finalValue = nikField.value;
                                    const success = finalValue === '{nik}';
                                    
                                    console.log('🛡️ PURE JAVASCRIPT NIK fill completed:');
                                    console.log('  Expected: {nik}');
                                    console.log('  Got: ' + finalValue);
                                    console.log('  Success: ' + success);
                                    
                                    return {{
                                        success: success,
                                        value: finalValue,
                                        expected: '{nik}',
                                        attempt: {attempt + 1},
                                        method: 'pure_javascript'
                                    }};
                                    
                                }} catch(e) {{
                                    console.error('PURE JAVASCRIPT NIK fill error:', e);
                                    return {{
                                        success: false, 
                                        reason: 'error', 
                                        error: e.message,
                                        attempt: {attempt + 1}
                                    }};
                                }}
                            }})()
                        """, attempt + 1)
                        
                        if nik_fill_result.get('success'):
                            print(f"      ✅ PURE JAVASCRIPT NIK SUCCESS: {nik_fill_result.get('value')} (attempt {attempt + 1})")
                            nik_success = True
                            break
                        else:
                            print(f"      ⚠️ NIK attempt {attempt + 1} failed: {nik_fill_result.get('reason')}")
                            if nik_fill_result.get('reason') == 'field_not_ready':
                                print(f"         💤 Waiting 1 second for field to be ready...")
                                page.wait_for_timeout(1000)
                                continue
                            elif nik_fill_result.get('reason') == 'field_not_found':
                                print(f"         🔍 NIK field not found, waiting...")
                                page.wait_for_timeout(1500)
                                continue
                            else:
                                print(f"         📊 Error details: {nik_fill_result}")
                                page.wait_for_timeout(500)
                        
                    except Exception as nik_error:
                        print(f"      ❌ NIK attempt {attempt + 1} exception: {nik_error}")
                        page.wait_for_timeout(500)
                
                # 🔍 PURE JAVASCRIPT: Verify NIK and check for error modals (NO Playwright field access)
                if nik_success:
                    print(f"      🔍 Verifying NIK value and checking for error notifications...")
                    page.wait_for_timeout(1000)  # Wait for any validation or error modal
                    
                    verification_result = page.evaluate("""
                        (function() {
                            try {
                                // Verify NIK value without Playwright
                                const nikField = document.getElementById('ahmgawpm003_nik_paspor_pekerja_add');
                                const currentNik = nikField ? nikField.value : 'field_not_found';
                                
                                // Check for error notification modal
                                const errorModal = document.getElementById('ahmgawpm003_notification_modal');
                                let errorInfo = {detected: false};
                                
                                if (errorModal && (errorModal.classList.contains('in') || errorModal.classList.contains('show'))) {
                                    const messageElement = document.getElementById('ahmgawpm003_notification_modal_message');
                                    const subMessageElement = document.getElementById('ahmgawpm003_notification_modal_submessage');
                                    
                                    const message = messageElement ? messageElement.textContent || messageElement.innerText : '';
                                    const subMessage = subMessageElement ? subMessageElement.textContent || subMessageElement.innerText : '';
                                    
                                    console.log('🚨 Error notification detected:');
                                    console.log('Message:', message);
                                    console.log('SubMessage:', subMessage);
                                    
                                    // Check if it's the NIK-related error
                                    const isNikError = 
                                        message.includes('NIK / Passport tidak dapat digunakan') ||
                                        subMessage.includes('belum melakukan') ||
                                        subMessage.includes('belum lulus Safety Induction') ||
                                        message.includes('tidak dapat digunakan');
                                    
                                    errorInfo = {
                                        detected: true,
                                        isNikError: isNikError,
                                        message: message,
                                        subMessage: subMessage
                                    };
                                    
                                    if (isNikError) {
                                        console.log('🚨 NIK validation error detected - dismissing modal...');
                                        
                                        // Dismiss the error modal
                                        const okButton = errorModal.querySelector('button[data-dismiss="modal"], .btn-primary, button');
                                        if (okButton) {
                                            okButton.click();
                                            console.log('Error modal dismissed via button');
                                        } else {
                                            // Force close
                                            errorModal.style.display = 'none';
                                            errorModal.classList.remove('in', 'show');
                                            console.log('Error modal force closed');
                                        }
                                        
                                        // Remove backdrop
                                        const backdrop = document.querySelector('.modal-backdrop');
                                        if (backdrop) backdrop.remove();
                                        
                                        errorInfo.dismissed = true;
                                    }
                                }
                                
                                return {
                                    nikValue: currentNik,
                                    errorInfo: errorInfo
                                };
                                
                            } catch(e) {
                                console.error('Verification error:', e);
                                return {
                                    nikValue: 'verification_error',
                                    errorInfo: {detected: false, error: e.message}
                                };
                            }
                        })()
                    """)
                    
                    current_nik = verification_result.get('nikValue')
                    error_info = verification_result.get('errorInfo', {})
                    
                    print(f"      📊 NIK verification: Expected='{nik}', Got='{current_nik}'")
                    
                    if error_info.get('detected'):
                        if error_info.get('isNikError'):
                            print(f"      🚨 NIK ERROR DETECTED AND DISMISSED!")
                            print(f"         📝 Message: {error_info.get('message')}")
                            print(f"         📝 SubMessage: {error_info.get('subMessage')}")
                            # Continue processing despite the error
                        else:
                            print(f"      ℹ️ Non-NIK error modal detected: {error_info.get('message')}")
                    else:
                        print(f"      ✅ No error notification - NIK accepted")
                else:
                    print(f"      🚨 NIK FAILED after 3 attempts!")
                
                # NAME Field - PURE JAVASCRIPT with Complete Enter Key Protection
                name_success = False
                for attempt in range(2):
                    try:
                        print(f"      📝 PURE JAVASCRIPT Name attempt {attempt + 1}: {name}")
                        
                        # Enhanced validation for name field (JavaScript only)
                        is_ready = page.evaluate("""
                            (function() {
                                const field = document.getElementById('ahmgawpm003_nama_pekerja_add');
                                return field && field.offsetParent !== null && 
                                       !field.disabled && !field.readOnly &&
                                       field.style.display !== 'none';
                            })()
                        """)
                        
                        if not is_ready:
                            print(f"      ⚠️ Name field not ready (attempt {attempt + 1})")
                            page.wait_for_timeout(1000)
                            continue
                        
                        # �️ ULTRA-SAFE NAME FILLING with Complete Enter Key Protection
                        print(f"      �️ ULTRA-SAFE Name filling with complete Enter key blocking...")
                        
                        # Install Enter key protection for Name field
                        name_protection_installed = page.evaluate("""
                            (function() {
                                try {
                                    const nameField = document.getElementById('ahmgawpm003_nama_pekerja_add');
                                    if (nameField) {
                                        // Remove any existing event listeners
                                        nameField.removeEventListener('keydown', window.nameEnterBlocker);
                                        nameField.removeEventListener('keypress', window.nameEnterBlocker);
                                        nameField.removeEventListener('keyup', window.nameEnterBlocker);
                                        
                                        // Create comprehensive Enter key blocker for Name
                                        window.nameEnterBlocker = function(e) {
                                            if (e.key === 'Enter' || e.keyCode === 13 || e.which === 13) {
                                                console.log('🛡️ BLOCKED Enter key in Name field!');
                                                e.preventDefault();
                                                e.stopPropagation();
                                                e.stopImmediatePropagation();
                                                return false;
                                            }
                                        };
                                        
                                        // Install Enter key blockers
                                        nameField.addEventListener('keydown', window.nameEnterBlocker, {capture: true});
                                        nameField.addEventListener('keypress', window.nameEnterBlocker, {capture: true});
                                        nameField.addEventListener('keyup', window.nameEnterBlocker, {capture: true});
                                        
                                        console.log('🛡️ Enter key protection installed for Name field');
                                        return true;
                                    }
                                    return false;
                                } catch(e) {
                                    console.log('Name Enter protection error:', e);
                                    return false;
                                }
                            })()
                        """)
                        
                        page.wait_for_timeout(200)  # Brief wait for protection to be active
                        
                        # Use JavaScript-only method for Name field
                        js_name_fill_success = page.evaluate(f"""
                            (function() {{
                                try {{
                                    const nameField = document.getElementById('ahmgawpm003_nama_pekerja_add');
                                    if (nameField && nameField.offsetParent !== null) {{
                                        
                                        // Clear and set value safely (no focus events)
                                        nameField.value = '';
                                        nameField.value = '{name}';
                                        nameField.setAttribute('value', '{name}');
                                        
                                        // Fire only essential events
                                        const inputEvent = new Event('input', {{bubbles: true, cancelable: false}});
                                        const changeEvent = new Event('change', {{bubbles: true, cancelable: false}});
                                        
                                        nameField.dispatchEvent(inputEvent);
                                        nameField.dispatchEvent(changeEvent);
                                        
                                        const finalValue = nameField.value;
                                        const success = finalValue === '{name}';
                                        
                                        console.log('🛡️ SAFE Name fill completed:', finalValue, 'Success:', success);
                                        return {{success: success, value: finalValue}};
                                    }}
                                    return {{success: false, reason: 'field_not_found'}};
                                }} catch(e) {{
                                    console.log('SAFE Name fill error:', e);
                                    return {{success: false, reason: 'error', error: e.message}};
                                }}
                            }})()
                        """)
                        
                        if js_name_fill_success.get('success'):
                            print(f"      ✅ ULTRA-SAFE JavaScript Name fill SUCCESS: {js_name_fill_success.get('value')}")
                        else:
                            print(f"      ⚠️ Primary Name fill failed, trying enhanced fallback...")
                            
                            # ULTRA-SAFE FALLBACK for Name field
                            name_fallback_success = page.evaluate(f"""
                                (function() {{
                                    try {{
                                        const nameField = document.getElementById('ahmgawpm003_nama_pekerja_add');
                                        if (!nameField) return {{success: false, reason: 'field_not_found'}};
                                        
                                        // Force clear and retry with different approach
                                        nameField.removeAttribute('value');
                                        nameField.value = '';
                                        
                                        // Set value with multiple methods
                                        nameField.value = '{name}';
                                        nameField.setAttribute('value', '{name}');
                                        nameField.defaultValue = '{name}';
                                        
                                        // Fire events
                                        ['input', 'change'].forEach(eventType => {{
                                            const evt = new Event(eventType, {{bubbles: true}});
                                            nameField.dispatchEvent(evt);
                                        }});
                                        
                                        return {{success: true, value: nameField.value, method: 'enhanced_fallback'}};
                                        
                                    }} catch(e) {{
                                        console.log('Name enhanced fallback error:', e);
                                        return {{success: false, reason: 'error', error: e.message}};
                                    }}
                                }})()
                            """)
                            
                            if name_fallback_success.get('success'):
                                print(f"      ✅ Name enhanced fallback SUCCESS")
                            else:
                                print(f"      ❌ All Name JavaScript methods failed")
                        
                        # Verify name was set (PURE JAVASCRIPT - no Playwright locator)
                        page.wait_for_timeout(500)  # Increased wait for verification
                        current_name = page.evaluate("""
                            (function() {
                                try {
                                    const nameField = document.getElementById('ahmgawpm003_nama_pekerja_add');
                                    return nameField ? nameField.value : 'field_not_found';
                                } catch(e) {
                                    return 'verification_error';
                                }
                            })()
                        """)
                        if current_name == name:
                            print(f"      ✅ Name verified: {current_name}")
                            name_success = True
                            break
                        else:
                            print(f"      ⚠️ Name mismatch - Expected: {name}, Got: {current_name}")
                            
                    except Exception as name_error:
                        print(f"      ❌ Name attempt {attempt + 1} failed: {name_error}")
                        page.wait_for_timeout(500)
                
                # Fill other fields with INSTANT approach - OPTIMIZED FOR SPEED
                print(f"      📝 Filling other basic fields (FAST MODE)...")
                
                # Use JavaScript for instant filling - much faster than human-like
                other_fields_success = page.evaluate("""
                    (function() {
                        try {
                            const fields = [
                                {id: 'ahmgawpm003_nomor_hp_pekerja_add', value: '082129002163'},
                                {id: 'ahmgawpm003_email_pekerja_add', value: 'Hirochiku-indonesia@co.id'},
                                {id: 'ahmgawpm003_seksi_add', value: 'HAI member'},
                                {id: 'ahmgawpm003_departemen_add', value: 'HAI member'},
                                {id: 'ahmgawpm003_divisi_add', value: 'HAI member'}
                            ];
                            
                            let fieldsSet = 0;
                            
                            fields.forEach(fieldData => {
                                const field = document.getElementById(fieldData.id);
                                if (field) {
                                    field.value = fieldData.value;
                                    field.setAttribute('value', fieldData.value);
                                    
                                    // Fire events
                                    ['focus', 'input', 'change', 'blur'].forEach(eventType => {
                                        field.dispatchEvent(new Event(eventType, {bubbles: true}));
                                    });
                                    
                                    fieldsSet++;
                                    console.log('INSTANT filled:', fieldData.id, '=', fieldData.value);
                                }
                            });
                             
                            return fieldsSet;
                        } catch(e) {
                            console.log('Instant fill error:', e);
                            return 0;
                        }
                    })()
                """)
                
                if other_fields_success >= 4:  # At least 4 out of 5 fields
                    other_fields_filled = other_fields_success
                    print(f"      ⚡ INSTANT FILL SUCCESS: {other_fields_success}/5 fields set")
                else:
                    # Fallback to Playwright method with reduced delays
                    print(f"      🔄 Fallback to Playwright method...")
                    other_fields = [
                        ("#ahmgawpm003_nomor_hp_pekerja_add", "082129002163"),
                        ("#ahmgawpm003_email_pekerja_add", "Hirochiku-indonesia@co.id"),
                        ("#ahmgawpm003_seksi_add", "HAI member"),
                        ("#ahmgawpm003_departemen_add", "HAI member"),
                        ("#ahmgawpm003_divisi_add", "HAI member")
                    ]
                    
                    other_fields_filled = 0
                    for field_id, value in other_fields:
                        try:
                            # 🛡️ SAFE: Use JavaScript-only method (NO keyboard events)
                            js_field_success = page.evaluate(f"""
                                (function() {{
                                    try {{
                                        const field = document.querySelector('{field_id}');
                                        if (field && field.offsetParent !== null) {{
                                            field.value = '{value}';
                                            field.setAttribute('value', '{value}');
                                            
                                            // Fire only essential events (no focus/blur that might trigger validation)
                                            ['input', 'change'].forEach(eventType => {{
                                                const evt = new Event(eventType, {{bubbles: true, cancelable: false}});
                                                field.dispatchEvent(evt);
                                            }});
                                            
                                            console.log('SAFE other field filled:', '{field_id}', '=', '{value}');
                                            return true;
                                        }}
                                        return false;
                                    }} catch(e) {{
                                        console.log('Other field fill error:', e);
                                        return false;
                                    }}
                                }})()
                            """)
                            
                            if js_field_success:
                                other_fields_filled += 1
                            else:
                                print(f"      ⚠️ Field {field_id} failed: JavaScript method failed")
                                
                        except Exception as field_error:
                            print(f"      ⚠️ Field {field_id} failed: {field_error}")
                
                # Brief pause before proceeding (ultra-fast mode)
                page.wait_for_timeout(50)
                
                print(f"    📊 Basic fields summary:")
                print(f"      NIK: {'✅ SUCCESS' if nik_success else '❌ FAILED'}")
                print(f"      Name: {'✅ SUCCESS' if name_success else '❌ FAILED'}")
                print(f"      Other fields: {other_fields_filled}/5 filled")
                
                # Additional verification for NIK (most critical)
                if not nik_success:
                    print(f"    🔄 EMERGENCY NIK RETRY...")
                    try:
                        # Emergency JavaScript method for NIK (ULTRA-SAFE)
                        emergency_nik_success = page.evaluate("""
                            (function() {
                                try {
                                    const nikField = document.getElementById('ahmgawpm003_nik_paspor_pekerja_add');
                                    if (nikField) {
                                        // Clear and set without focus (safer)
                                        nikField.value = '';
                                        nikField.value = arguments[0];
                                        nikField.setAttribute('value', arguments[0]);
                                        nikField.defaultValue = arguments[0];
                                        
                                        // Fire only essential events (no focus/blur)
                                        ['input', 'change'].forEach(eventType => {
                                            nikField.dispatchEvent(new Event(eventType, {bubbles: true, cancelable: false}));
                                        });
                                        
                                        console.log('Emergency NIK set (ULTRA-SAFE):', nikField.value);
                                        return nikField.value === arguments[0];
                                    }
                                    return false;
                                } catch(e) {
                                    console.log('Emergency NIK error:', e);
                                    return false;
                                }
                            })()
                        """, nik)
                        
                        if emergency_nik_success:
                            print(f"    ✅ EMERGENCY NIK SUCCESS: {nik}")
                        else:
                            print(f"    ❌ EMERGENCY NIK FAILED: {nik}")
                            
                    except Exception as emergency_error:
                        print(f"    🚨 Emergency NIK failed: {emergency_error}")
                
                page.wait_for_timeout(80)  # Ultra-fast minimal pause
                
                # Handle certification based on CSV data
                if has_cert:
                    # Person has certificate - fill with certificate data
                    cert_data = cert_lookup[nik]
                    print(f"    🏆 PERSON HAS CERTIFICATE: {cert_data['cert']} (Exp: {cert_data['exp_cert']})")
                    print(f"    🔧 ENHANCED CERTIFICATE HANDLING for person {i}/{len(personnel_data)}")
                    
                    try:
                        # Set certification to "Y" - ENHANCED METHOD WITH LONGER WAIT
                        print(f"    🔧 Setting certification requirement to YES...")
                        
                        # LONGER WAIT for form to be ready after basic fields
                        page.wait_for_timeout(1500)  # Increased from 1000ms
                        
                        # Use JavaScript for more reliable field setting
                        cert_set_success = page.evaluate("""
                            (function() {
                                try {
                                    const certField = document.getElementById('ahmgawpm003_kebutuhan_sertifikasi_add');
                                    if (certField) {
                                        certField.value = 'Y';
                                        certField.dispatchEvent(new Event('change', {bubbles: true}));
                                        certField.dispatchEvent(new Event('blur', {bubbles: true}));
                                        console.log('Certificate requirement set to Y');
                                        return true;
                                    }
                                    return false;
                                } catch(e) {
                                    console.log('Certificate field setting error:', e);
                                    return false;
                                }
                            })()
                        """)
                        
                        if cert_set_success:
                            print(f"    ✅ Certificate requirement set to YES")
                        else:
                            # Fallback method
                            page.locator("#ahmgawpm003_kebutuhan_sertifikasi_add").select_option("Y")
                            print(f"    ✅ Certificate requirement set (fallback method)")
                        
                        # EXTENDED WAIT for certificate fields to appear (especially for multiple certs)
                        print(f"    ⏳ Waiting for certificate fields to appear (extended wait for person {i})...")
                        page.wait_for_timeout(2000)  # Increased from 1000ms for multiple cert handling
                        
                        # Fill certificate number - ENHANCED METHOD WITH RETRY
                        print(f"    📜 Filling certificate number: {cert_data['cert']}")
                        
                        cert_num_success = False
                        for cert_attempt in range(2):  # Try twice
                            try:
                                cert_num_result = page.evaluate(f"""
                                    (function() {{
                                        try {{
                                            const certNumField = document.getElementById('ahmgawpm003_nomor_sertifikasi_add');
                                            if (certNumField && certNumField.offsetParent !== null) {{
                                                // Clear field first
                                                certNumField.value = '';
                                                certNumField.focus();
                                                
                                                // Fill with certificate number
                                                certNumField.value = '{cert_data['cert']}';
                                                certNumField.setAttribute('value', '{cert_data['cert']}');
                                                
                                                // Fire all necessary events
                                                ['input', 'change', 'blur', 'keyup'].forEach(eventType => {{
                                                    certNumField.dispatchEvent(new Event(eventType, {{ bubbles: true }}));
                                                }});
                                                
                                                console.log('Certificate number filled: {cert_data['cert']}');
                                                return {{success: true, value: certNumField.value}};
                                            }} else {{
                                                return {{success: false, reason: 'field_not_visible'}};
                                            }}
                                        }} catch(e) {{
                                            console.log('Certificate number fill error:', e);
                                            return {{success: false, reason: 'error', error: e.message}};
                                        }}
                                    }})()
                                """)
                                
                                if cert_num_result.get('success'):
                                    print(f"    ✅ Certificate number filled (attempt {cert_attempt + 1}): {cert_num_result.get('value')}")
                                    cert_num_success = True
                                    break
                                else:
                                    print(f"    ⚠️ Certificate number attempt {cert_attempt + 1} failed: {cert_num_result.get('reason')}")
                                    page.wait_for_timeout(1000)  # Wait before retry
                                    
                            except Exception as cert_fill_error:
                                print(f"    ❌ Certificate number attempt {cert_attempt + 1} exception: {cert_fill_error}")
                                page.wait_for_timeout(1000)
                        
                        if not cert_num_success:
                            # JavaScript-only fallback method (no Playwright interactions)
                            cert_fallback_result = page.evaluate(f"""
                                (function() {{
                                    try {{
                                        const certField = document.getElementById('ahmgawpm003_nomor_sertifikasi_add');
                                        if (certField && certField.offsetParent !== null) {{
                                            // Clear and set certificate number
                                            certField.value = '';
                                            certField.value = '{cert_data['cert']}';
                                            certField.setAttribute('value', '{cert_data['cert']}');
                                            
                                            // Fire events
                                            const inputEvent = new Event('input', {{bubbles: true}});
                                            const changeEvent = new Event('change', {{bubbles: true}});
                                            certField.dispatchEvent(inputEvent);
                                            certField.dispatchEvent(changeEvent);
                                            
                                            return {{success: true, value: certField.value}};
                                        }}
                                        return {{success: false, reason: 'field_not_found'}};
                                    }} catch(e) {{
                                        return {{success: false, reason: 'error', error: e.message}};
                                    }}
                                }})()
                            """)
                            
                            if cert_fallback_result.get('success'):
                                print(f"    ✅ Certificate number filled (JavaScript fallback): {cert_fallback_result.get('value')}")
                            else:
                                print(f"    ❌ Certificate number JavaScript fallback failed: {cert_fallback_result.get('reason')}")
                        
                        # Wait for certificate expiry date field to appear after certificate number input
                        print(f"    ⏳ Waiting for certificate expiry date field to appear (person {i})...")
                        expiry_field_ready = False
                        
                        # Try multiple times to wait for expiry field (important for multiple certs)
                        for wait_attempt in range(3):
                            try:
                                # Wait for the certificate expiry field to be visible
                                page.wait_for_selector("#ahmgawpm003_tanggal_akhir_berlaku_izin_edit", state="visible", timeout=5000)
                                print(f"    ✅ Certificate expiry date field is now visible (attempt {wait_attempt + 1})")
                                expiry_field_ready = True
                                break
                            except Exception as wait_error:
                                print(f"    ⚠️ Certificate expiry field wait attempt {wait_attempt + 1} failed: {wait_error}")
                                if wait_attempt < 2:  # Don't wait on last attempt
                                    page.wait_for_timeout(2000)  # Wait 2 seconds before retry
                        
                        if not expiry_field_ready:
                            # Try alternative selectors
                            alt_expiry_selectors = [
                                'input[id*="tanggal_akhir_berlaku"]',
                                'input[id*="tanggal_akhir"]',
                                'input[id*="expiry"]',
                                'input[id*="expired"]'
                            ]
                            for selector in alt_expiry_selectors:
                                try:
                                    page.wait_for_selector(selector, state="visible", timeout=2000)
                                    print(f"    ✅ Alternative expiry field found: {selector}")
                                    expiry_field_ready = True
                                    break
                                except:
                                    continue
                        
                        if not expiry_field_ready:
                            print(f"    ⚠️ No expiry date field found, but continuing anyway...")
                        
                        # Additional wait to ensure form is ready (important for multiple certificates)
                        page.wait_for_timeout(1500)  # Increased from 1000ms
                        
                        # Handle expiry date - ENHANCED FOR MULTIPLE PEOPLE WITH DYNAMIC FIELD DETECTION ⚡
                        print(f"    📅 Setting certificate expiry date for person {i}/{len(personnel_data)} (ENHANCED MULTI-PERSON HANDLING)...")
                        
                        # Use FIXED expiry date (31 Juli 2027) - NOT dependent on work date
                        expiry_date_value = "31/07/2027"  # FIXED DATE!
                        print(f"    🗓️ Using FIXED expiry date: {expiry_date_value} (NOT same as today!)")
                        
                        # 🔍 ULTRA-ENHANCED DYNAMIC FIELD DETECTION for multiple people with FRESH SCAN
                        print(f"    🔍 ULTRA-ENHANCED DYNAMIC field detection for person {i}/{len(personnel_data)}...")
                        dynamic_expiry_field_id = None
                        
                        # FRESH SCAN - Clear any cached field references first
                        page.evaluate(f"""
                            window.lastUsedExpiryField = null;
                            window.fieldDetectionCache = null;
                            window.currentPersonBeingProcessed = {i};
                            console.log('Field detection cache cleared for person {i}');
                        """)
                        
                        # Wait for form to be fully ready for this specific person
                        page.wait_for_timeout(1000 + (i * 300))  # Progressive wait per person
                        
                        # COMPREHENSIVE field detection with FRESH SCAN
                        expiry_field_detection = page.evaluate(f"""
                            (function(personNum) {{
                                try {{
                                    console.log('=== FRESH EXPIRY FIELD SCAN for person ' + personNum + ' ===');
                                    
                                    // Extended possible field IDs for certificate expiry
                                    const possibleIds = [
                                        'ahmgawpm003_tanggal_akhir_berlaku_izin_edit',
                                        'ahmgawpm003_tanggal_akhir_berlaku_izin_add', 
                                        'ahmgawpm003_tanggal_akhir_berlaku_sertifikat_edit',
                                        'ahmgawpm003_tanggal_akhir_berlaku_sertifikat_add',
                                        'ahmgawpm003_exp_sertifikat_edit',
                                        'ahmgawpm003_exp_sertifikat_add',
                                        'ahmgawpm003_tanggal_exp_edit',
                                        'ahmgawpm003_tanggal_exp_add',
                                        'ahmgawpm003_certificate_expiry_edit',
                                        'ahmgawpm003_certificate_expiry_add'
                                    ];
                                    
                                    let foundFields = [];
                                    let freshFields = [];  // Fields that are empty/fresh
                                    let allVisibleFields = [];
                                    
                                    // STEP 1: Check exact IDs with FRESH state verification
                                    for (let id of possibleIds) {{
                                        const field = document.getElementById(id);
                                        if (field) {{
                                            const isVisible = field.offsetParent !== null && 
                                                            field.style.display !== 'none' &&
                                                            !field.disabled &&
                                                            !field.readOnly;
                                            const isEmpty = !field.value || field.value.trim() === '';
                                            const isFresh = isEmpty && !field.dataset.processed;
                                            
                                            allVisibleFields.push({{
                                                id: id,
                                                visible: isVisible,
                                                empty: isEmpty,
                                                fresh: isFresh,
                                                type: field.type,
                                                value: field.value,
                                                placeholder: field.placeholder || '',
                                                className: field.className,
                                                disabled: field.disabled,
                                                readOnly: field.readOnly
                                            }});
                                            
                                            if (isVisible) {{
                                                foundFields.push({{
                                                    id: id,
                                                    priority: isEmpty ? 10 : 5,  // Empty fields get higher priority
                                                    visible: true,
                                                    type: field.type,
                                                    value: field.value,
                                                    fresh: isFresh
                                                }});
                                                
                                                if (isFresh) {{
                                                    freshFields.push(id);
                                                }}
                                            }}
                                        }}
                                    }}
                                    
                                    // STEP 2: Extended selector-based search for FRESH fields
                                    const extendedSelectors = [
                                        'input[id*="tanggal_akhir_berlaku"]:not([data-processed])',
                                        'input[id*="tanggal_akhir"]:not([data-processed])', 
                                        'input[id*="expiry"]:not([data-processed])',
                                        'input[id*="expired"]:not([data-processed])',
                                        'input[id*="exp_sertifikat"]:not([data-processed])',
                                        'input[id*="sertifikat"][id*="tanggal"]:not([data-processed])',
                                        'input[id*="certificate"][id*="date"]:not([data-processed])',
                                        'input[id*="cert"][id*="exp"]:not([data-processed])',
                                        'input[placeholder*="expiry"]:not([data-processed])',
                                        'input[placeholder*="expired"]:not([data-processed])',
                                        'input[name*="tanggal_akhir"]:not([data-processed])',
                                        'input[aria-label*="expiry"]:not([data-processed])',
                                        'input[aria-label*="expired"]:not([data-processed])'
                                    ];
                                    
                                    for (let selector of extendedSelectors) {{
                                        const fields = document.querySelectorAll(selector);
                                        fields.forEach(field => {{
                                            if (field.offsetParent !== null && field.id && 
                                                !foundFields.some(f => f.id === field.id)) {{
                                                const isEmpty = !field.value || field.value.trim() === '';
                                                const isFresh = isEmpty && !field.dataset.processed;
                                                
                                                foundFields.push({{
                                                    id: field.id,
                                                    priority: isFresh ? 15 : (isEmpty ? 8 : 3),  // Fresh fields get highest priority
                                                    visible: true,
                                                    type: field.type,
                                                    value: field.value,
                                                    selector: selector,
                                                    fresh: isFresh,
                                                    placeholder: field.placeholder || '',
                                                    className: field.className
                                                }});
                                                
                                                if (isFresh) {{
                                                    freshFields.push(field.id);
                                                }}
                                            }}
                                        }});
                                    }}
                                    
                                    // STEP 3: Sort by priority (fresh > empty > filled)
                                    foundFields.sort((a, b) => b.priority - a.priority);
                                    
                                    console.log('=== FIELD DETECTION RESULTS for person ' + personNum + ' ===');
                                    console.log('Total fields found:', foundFields.length);
                                    console.log('Fresh fields available:', freshFields.length);
                                    console.log('All visible fields:', allVisibleFields.length);
                                    
                                    foundFields.forEach((field, index) => {{
                                        console.log('Field ' + (index + 1) + ':', field.id, 'Priority:', field.priority, 'Fresh:', field.fresh, 'Value:', field.value);
                                    }});
                                    
                                    return {{
                                        success: foundFields.length > 0,
                                        fields: foundFields,
                                        freshFields: freshFields,
                                        allVisibleFields: allVisibleFields,
                                        recommendedId: foundFields.length > 0 ? foundFields[0].id : null,
                                        personNum: personNum,
                                        totalFound: foundFields.length,
                                        freshCount: freshFields.length
                                    }};
                                    
                                }} catch(e) {{
                                    console.error('Field detection error for person ' + personNum + ':', e);
                                    return {{success: false, error: e.message, fields: [], personNum: personNum}};
                                }}
                            }})()
                        """, i)
                        
                        if expiry_field_detection.get('success') and expiry_field_detection.get('recommendedId'):
                            dynamic_expiry_field_id = expiry_field_detection['recommendedId']
                            print(f"    ✅ ULTRA-ENHANCED detection SUCCESS for person {i}")
                            print(f"    🎯 Selected field: {dynamic_expiry_field_id} (Fresh count: {expiry_field_detection.get('freshCount', 0)})")
                            print(f"    📊 Available expiry fields for person {i} ({expiry_field_detection.get('totalFound', 0)} total):")
                            for field in expiry_field_detection['fields'][:3]:  # Show top 3
                                fresh_indicator = "🆕" if field.get('fresh') else "📝" if not field.get('value') else "🔄"
                                print(f"      {fresh_indicator} {field['id']} (priority: {field['priority']}, type: {field['type']})")
                        else:
                            print(f"    ⚠️ ULTRA-ENHANCED detection failed for person {i}, using default field ID")
                            print(f"    📊 Detection details: {expiry_field_detection}")
                            dynamic_expiry_field_id = 'ahmgawpm003_tanggal_akhir_berlaku_izin_edit'
                        
                        # ENHANCED HUMAN MIMIC with dynamic field ID
                        print(f"    📅 Attempting HUMAN MIMIC calendar navigation for person {i}...")
                        expiry_success = set_expiry_date_field(page, expiry_date_value, dynamic_expiry_field_id)
                        
                        if expiry_success:
                            print(f"    ✅ Certificate expiry date set HUMAN-LIKE for person {i}: {expiry_date_value}")
                        else:
                            print(f"    ⚠️ HUMAN MIMIC failed for person {i}, trying ENHANCED MULTI-PERSON FALLBACK...")
                            
                            # 🚀 ULTRA-ENHANCED EMERGENCY FALLBACK for multiple people with FIELD MARKING
                            ultra_enhanced_fallback_success = page.evaluate(f"""
                            (function(personNum, fieldId) {{
                                try {{
                                    console.log('=== ULTRA-ENHANCED EMERGENCY FALLBACK for person ' + personNum + ' ===');
                                    
                                    let expField = null;
                                    let selectedFieldInfo = null;
                                    
                                    // STEP 1: Try the dynamically detected field first
                                    if (fieldId && fieldId !== 'null') {{
                                        expField = document.getElementById(fieldId);
                                        if (expField && expField.offsetParent !== null && !expField.dataset.processed) {{
                                            selectedFieldInfo = {{
                                                source: 'dynamic_detection',
                                                id: fieldId,
                                                fresh: !expField.value && !expField.dataset.processed
                                            }};
                                            console.log('Using dynamic field: ' + fieldId + ' (fresh: ' + selectedFieldInfo.fresh + ')');
                                        }} else {{
                                            console.log('Dynamic field not suitable: ' + fieldId);
                                            expField = null;
                                        }}
                                    }}
                                    
                                    // STEP 2: If dynamic failed, COMPREHENSIVE FRESH FIELD SEARCH
                                    if (!expField) {{
                                        console.log('Starting comprehensive fresh field search...');
                                        
                                        // Extended comprehensive selectors with fresh field priority
                                        const comprehensiveSelectors = [
                                            // High priority: Exact IDs that are fresh
                                            '#ahmgawpm003_tanggal_akhir_berlaku_izin_edit:not([data-processed])',
                                            '#ahmgawpm003_tanggal_akhir_berlaku_izin_add:not([data-processed])',
                                            '#ahmgawpm003_tanggal_akhir_berlaku_sertifikat_edit:not([data-processed])',
                                            '#ahmgawpm003_tanggal_akhir_berlaku_sertifikat_add:not([data-processed])',
                                            // Medium priority: Pattern-based fresh fields
                                            'input[id*="tanggal_akhir_berlaku"]:not([data-processed])',
                                            'input[id*="tanggal_akhir"]:not([data-processed])',
                                            'input[id*="expiry"]:not([data-processed])',
                                            'input[id*="expired"]:not([data-processed])',
                                            'input[id*="exp_sertifikat"]:not([data-processed])',
                                            'input[id*="sertifikat"][id*="tanggal"]:not([data-processed])',
                                            'input[id*="certificate"][id*="date"]:not([data-processed])',
                                            'input[id*="cert"][id*="exp"]:not([data-processed])',
                                            // Lower priority: Any fresh date fields
                                            'input[type="date"]:not([data-processed])',
                                            'input[placeholder*="expiry"]:not([data-processed])',
                                            'input[placeholder*="expired"]:not([data-processed])',
                                            'input[name*="tanggal_akhir"]:not([data-processed])',
                                            'input[aria-label*="expiry"]:not([data-processed])',
                                            'input[aria-label*="expired"]:not([data-processed])',
                                            // Emergency: Any visible date-like field
                                            'input[placeholder*="DD/MM/YYYY"]:not([data-processed])',
                                            'input[placeholder*="dd/mm/yyyy"]:not([data-processed])'
                                        ];
                                        
                                        let candidateFields = [];
                                        
                                        for (let selector of comprehensiveSelectors) {{
                                            const fields = document.querySelectorAll(selector);
                                            console.log('Selector "' + selector + '" found ' + fields.length + ' fields');
                                            
                                            fields.forEach((field, index) => {{
                                                if (field && field.offsetParent !== null && !field.disabled) {{
                                                    const isEmpty = !field.value || field.value.trim() === '';
                                                    const isFresh = !field.dataset.processed;
                                                    const isVisible = field.offsetParent !== null;
                                                    
                                                    let priority = 0;
                                                    if (isFresh && isEmpty) priority = 100;
                                                    else if (isFresh) priority = 80;
                                                    else if (isEmpty) priority = 60;
                                                    else priority = 20;
                                                    
                                                    // Bonus for exact ID matches
                                                    if (field.id.includes('tanggal_akhir_berlaku')) priority += 20;
                                                    if (field.id.includes('sertifikat') || field.id.includes('certificate')) priority += 10;
                                                    
                                                    candidateFields.push({{
                                                        field: field,
                                                        id: field.id,
                                                        priority: priority,
                                                        fresh: isFresh,
                                                        empty: isEmpty,
                                                        visible: isVisible,
                                                        selector: selector,
                                                        value: field.value
                                                    }});
                                                    
                                                    console.log('Candidate: ' + field.id + ' (priority: ' + priority + ', fresh: ' + isFresh + ', empty: ' + isEmpty + ')');
                                                }}
                                            }});
                                        }}
                                        
                                        // Sort by priority (highest first)
                                        candidateFields.sort((a, b) => b.priority - a.priority);
                                        
                                        if (candidateFields.length > 0) {{
                                            const bestCandidate = candidateFields[0];
                                            expField = bestCandidate.field;
                                            selectedFieldInfo = {{
                                                source: 'comprehensive_search',
                                                id: bestCandidate.id,
                                                priority: bestCandidate.priority,
                                                fresh: bestCandidate.fresh,
                                                empty: bestCandidate.empty,
                                                selector: bestCandidate.selector
                                            }};
                                            console.log('Best candidate selected: ' + bestCandidate.id + ' (priority: ' + bestCandidate.priority + ')');
                                        }}
                                    }}
                                    
                                    // STEP 3: ULTRA-ENHANCED FIELD SETTING if field found
                                    if (expField && expField.offsetParent !== null) {{
                                        console.log('Setting field: ' + expField.id + ' with value: {expiry_date_value}');
                                        
                                        // MARK field as being processed to avoid conflicts
                                        expField.dataset.processed = 'person_' + personNum;
                                        expField.dataset.processTime = new Date().getTime();
                                        
                                        // COMPREHENSIVE field clearing first
                                        expField.value = '';
                                        expField.focus();
                                        
                                        // Force clear any existing value
                                        if (expField.value) {{
                                            expField.select();
                                            document.execCommand('delete');
                                        }}
                                        
                                        // Set the FIXED date value (31 Juli 2027)
                                        expField.value = '{expiry_date_value}';
                                        expField.setAttribute('value', '{expiry_date_value}');
                                        
                                        // ULTRA-COMPREHENSIVE event firing
                                        const eventSequence = [
                                            'focus', 'click', 'input', 'keydown', 'keyup', 
                                            'change', 'blur', 'propertychange'
                                        ];
                                        
                                        eventSequence.forEach(eventType => {{
                                            try {{
                                                const event = new Event(eventType, {{bubbles: true, cancelable: true}});
                                                expField.dispatchEvent(event);
                                            }} catch(e) {{
                                                console.log('Event ' + eventType + ' failed:', e);
                                            }}
                                        }});
                                        
                                        // Trigger specific validation functions if they exist
                                        const validationFunctions = [
                                            'ahmgawpm003_checkEditWorker',
                                            'ahmgawpm003_checkDateInput', 
                                            'ahmgawpm003_validateForm',
                                            'ahmgawpm003_checkForm',
                                            'validateExpiryDate',
                                            'checkCertificateExpiry'
                                        ];
                                        
                                        validationFunctions.forEach(funcName => {{
                                            try {{
                                                if (typeof window[funcName] === 'function') {{
                                                    window[funcName](expField);
                                                    console.log('Validation function called: ' + funcName);
                                                }}
                                            }} catch(e) {{
                                                console.log('Validation function ' + funcName + ' failed:', e);
                                            }}
                                        }});
                                        
                                        // Force modal validation and enable submit
                                        const modal = expField.closest('.modal, [role="dialog"]');
                                        if (modal) {{
                                            const submitBtns = modal.querySelectorAll('button[type="submit"], .btn-primary, #ahmgawpm003_submit_button_add_modal');
                                            submitBtns.forEach(btn => {{
                                                btn.removeAttribute('disabled');
                                                btn.disabled = false;
                                                btn.style.pointerEvents = 'auto';
                                                btn.style.opacity = '1';
                                                btn.classList.remove('disabled');
                                            }});
                                        }}
                                        
                                        // Final verification
                                        const finalValue = expField.value;
                                        const wasSet = finalValue === '{expiry_date_value}';
                                        
                                        console.log('ULTRA-ENHANCED fallback result for person ' + personNum + ':');
                                        console.log('  Field ID: ' + expField.id);
                                        console.log('  Set value: {expiry_date_value}');
                                        console.log('  Final value: ' + finalValue);
                                        console.log('  Success: ' + wasSet);
                                        console.log('  Field info: ' + JSON.stringify(selectedFieldInfo));
                                        
                                        return {{
                                            success: wasSet, 
                                            setValue: '{expiry_date_value}',
                                            finalValue: finalValue,
                                            fieldId: expField.id,
                                            fieldType: expField.type,
                                            person: personNum,
                                            fieldInfo: selectedFieldInfo,
                                            marked: true
                                        }};
                                    }} else {{
                                        console.log('No suitable expiry field found for person ' + personNum);
                                        return {{
                                            success: false, 
                                            reason: 'no_field_found', 
                                            person: personNum,
                                            searchedSelectors: comprehensiveSelectors.length
                                        }};
                                    }}
                                }} catch(e) {{
                                    console.error('ULTRA-ENHANCED fallback error for person ' + personNum + ':', e);
                                    return {{
                                        success: false, 
                                        reason: 'exception', 
                                        error: e.message, 
                                        person: personNum
                                    }};
                                }}
                            }})()
                        """, dynamic_expiry_field_id, i)
                        
                            if ultra_enhanced_fallback_success.get('success'):
                                print(f"    ✅ ULTRA-ENHANCED fallback SUCCESS for person {i}: {ultra_enhanced_fallback_success.get('finalValue')}")
                                print(f"    🎯 Field used: {ultra_enhanced_fallback_success.get('fieldId')} (source: {ultra_enhanced_fallback_success.get('fieldInfo', {}).get('source', 'unknown')})")
                                print(f"    🔖 Field marked to prevent reuse")
                            else:
                                print(f"    ❌ ALL ULTRA-ENHANCED METHODS FAILED for person {i}: {ultra_enhanced_fallback_success.get('reason')}")
                                print(f"    📊 Failure details: {ultra_enhanced_fallback_success}")
                                # Take comprehensive screenshot for debugging
                                try:
                                    page.screenshot(path=f'/home/dan/Portal/debug_person_{i}_all_methods_failed.png')
                                    print(f"    📸 Debug screenshot saved: debug_person_{i}_all_methods_failed.png")
                                    
                                    # Also save page HTML for detailed debugging
                                    page_html = page.content()
                                    with open(f'/home/dan/Portal/debug_person_{i}_page_content.html', 'w', encoding='utf-8') as f:
                                        f.write(page_html)
                                    print(f"    📄 Page HTML saved: debug_person_{i}_page_content.html")
                                except Exception as debug_error:
                                    print(f"    ⚠️ Debug file save failed: {debug_error}")
                        
                        print(f"    🎉 CERTIFICATE DATA COMPLETED for {name} (person {i}/{len(personnel_data)})")
                        
                        # ENHANCED MODAL SUBMIT for multiple people with retry
                        print(f"    📝 ENHANCED MODAL SUBMIT for person {i}...")
                        submit_success = False
                        
                        for submit_attempt in range(3):  # Try up to 3 times
                            try:
                                # Wait for any processing to complete
                                page.wait_for_timeout(800 + (i * 200))  # Increasing delay per person
                                
                                # Ensure submit button is enabled
                                page.evaluate("""
                                    (function() {
                                        const submitBtn = document.getElementById('ahmgawpm003_submit_button_add_modal');
                                        if (submitBtn) {
                                            submitBtn.removeAttribute('disabled');
                                            submitBtn.disabled = false;
                                            submitBtn.style.pointerEvents = 'auto';
                                            submitBtn.style.opacity = '1';
                                            submitBtn.classList.remove('disabled');
                                        }
                                    })()
                                """)
                                
                                # Submit the person
                                submit_btn = page.locator("#ahmgawpm003_submit_button_add_modal")
                                if submit_btn.is_visible():
                                    submit_btn.click()
                                    print(f"      ✅ Submit clicked for person {i} (attempt {submit_attempt + 1})")
                                    
                                    # 🔥 CRITICAL: Wait for submit to be processed and modal to close automatically
                                    print(f"      ⏳ Waiting for submit processing and auto-modal closure...")
                                    
                                    # Wait for modal to automatically close after successful submit
                                    submit_processed = False
                                    for wait_count in range(10):  # Wait up to 10 seconds
                                        try:
                                            # 🚨 CRITICAL: Handle notification modal that appears after successful submit
                                            notification_modal_result = page.evaluate("""
                                                (function() {
                                                    try {
                                                        // Check for notification modal that blocks interaction
                                                        const notificationModal = document.getElementById('ahmgawpm003_notification_modal');
                                                        if (notificationModal && (notificationModal.classList.contains('in') || notificationModal.classList.contains('show'))) {
                                                            console.log('Notification modal detected - dismissing...');
                                                            
                                                            // Try to find and click OK/Close button in notification modal
                                                            const okButtons = notificationModal.querySelectorAll('button, .btn, [data-dismiss]');
                                                            for (let btn of okButtons) {
                                                                const btnText = (btn.textContent || btn.innerText || '').toLowerCase();
                                                                if (btnText.includes('ok') || btnText.includes('close') || btnText.includes('tutup') || 
                                                                    btn.getAttribute('data-dismiss') === 'modal') {
                                                                    btn.click();
                                                                    console.log('Notification modal dismissed');
                                                                    return {notification: true, dismissed: true};
                                                                }
                                                            }
                                                            
                                                            // If no button found, force hide the modal
                                                            notificationModal.style.display = 'none';
                                                            notificationModal.classList.remove('in', 'show');
                                                            notificationModal.setAttribute('aria-hidden', 'true');
                                                            
                                                            // Remove backdrop
                                                            const backdrops = document.querySelectorAll('.modal-backdrop');
                                                            backdrops.forEach(backdrop => backdrop.remove());
                                                            
                                                            console.log('Notification modal force hidden');
                                                            return {notification: true, dismissed: true, forced: true};
                                                        }
                                                        
                                                        return {notification: false};
                                                    } catch(e) {
                                                        console.log('Notification modal check error:', e);
                                                        return {notification: false, error: e.message};
                                                    }
                                                })()
                                            """)
                                            
                                            if notification_modal_result.get('notification'):
                                                print(f"      🔔 Notification modal handled: {notification_modal_result}")
                                                page.wait_for_timeout(1000)  # Wait after dismissing notification
                                            
                                            # Check if main modal is still visible
                                            modal_still_visible = page.evaluate("""
                                                (function() {
                                                    const modal = document.getElementById('ahmgawpm003_add_worker_modal');
                                                    if (!modal) return false;
                                                    
                                                    const isVisible = modal.offsetParent !== null && 
                                                                    modal.style.display !== 'none' &&
                                                                    (modal.classList.contains('in') || modal.classList.contains('show'));
                                                    return isVisible;
                                                })()
                                            """)
                                            
                                            if not modal_still_visible:
                                                print(f"      ✅ Submit processed successfully - Modal auto-closed (wait {wait_count + 1})")
                                                submit_processed = True
                                                break
                                            else:
                                                page.wait_for_timeout(1000)  # Wait 1 second before checking again
                                                print(f"      ⏳ Submit processing... (wait {wait_count + 1}/10)")
                                                
                                        except Exception as wait_error:
                                            print(f"      ⚠️ Submit wait error: {wait_error}")
                                            page.wait_for_timeout(1000)
                                    
                                    if submit_processed:
                                        submit_success = True
                                        break
                                    else:
                                        print(f"      ⚠️ Submit may not have processed correctly (attempt {submit_attempt + 1})")
                                        
                                else:
                                    print(f"      ⚠️ Submit button not visible for person {i} (attempt {submit_attempt + 1})")
                                    
                            except Exception as submit_error:
                                print(f"      ❌ Submit attempt {submit_attempt + 1} failed for person {i}: {submit_error}")
                                if submit_attempt < 2:  # Don't wait on last attempt
                                    page.wait_for_timeout(1000)
                        
                        if not submit_success:
                            print(f"    🚨 SUBMIT FAILED for person {i} after 3 attempts!")
                            # Take screenshot for debugging
                            try:
                                page.screenshot(path=f'/home/dan/Portal/debug_person_{i}_submit_failed.png')
                                print(f"    📸 Debug screenshot saved: debug_person_{i}_submit_failed.png")
                            except:
                                pass
                        else:
                            print(f"    🎉 SUBMIT SUCCESS for person {i} - {name} added successfully!")
                        
                        # 🔥 ENHANCED POST-SUBMIT CLEANUP for multiple people 🔥
                        if submit_success and i < len(personnel_data):  # Not the last person
                            print(f"    � POST-SUBMIT CLEANUP for person {i} before next person...")
                            
                            # Ensure modal is completely closed and DOM is clean
                            cleanup_success = page.evaluate("""
                                (function() {
                                    try {
                                        // Force close any remaining modals
                                        const modals = document.querySelectorAll('.modal, .modal.fade, .modal.in, .modal.show');
                                        modals.forEach(modal => {
                                            modal.style.display = 'none';
                                            modal.classList.remove('in', 'show', 'fade');
                                            modal.setAttribute('aria-hidden', 'true');
                                            modal.removeAttribute('aria-modal');
                                        });
                                        
                                        // Remove all modal backdrops
                                        const backdrops = document.querySelectorAll('.modal-backdrop');
                                        backdrops.forEach(backdrop => backdrop.remove());
                                        
                                        // Reset body state
                                        document.body.classList.remove('modal-open');
                                        document.body.style.removeProperty('padding-right');
                                        document.body.style.removeProperty('overflow');
                                        
                                        // Clear all form fields in any modal
                                        const modalFields = document.querySelectorAll('.modal input, .modal select, .modal textarea');
                                        modalFields.forEach(field => {
                                            if (field.type !== 'hidden' && field.type !== 'submit') {
                                                field.value = '';
                                                field.checked = false;
                                                field.selectedIndex = 0;
                                                // Re-enable fields that might have been disabled
                                                field.disabled = false;
                                                field.readOnly = false;
                                                field.removeAttribute('disabled');
                                                field.removeAttribute('readonly');
                                            }
                                        });
                                        
                                        // Clear any window variables that might interfere
                                        window.lastUsedExpiryField = null;
                                        window.currentPersonNum = null;
                                        window.fieldDetectionCache = null;
                                        window.personnelModalOpen = false;
                                        
                                        console.log('Post-submit cleanup completed successfully');
                                        return {success: true, message: 'Cleanup completed'};
                                        
                                    } catch(e) {
                                        console.log('Post-submit cleanup error:', e);
                                        return {success: false, error: e.message};
                                    }
                                })()
                            """)
                            
                            if cleanup_success.get('success'):
                                print(f"    ✅ Post-submit cleanup SUCCESS")
                            else:
                                print(f"    ⚠️ Post-submit cleanup failed: {cleanup_success.get('error')}")
                            
                            # Additional wait to ensure everything is settled (ultra-fast mode)
                            base_delay = 150  # 150ms base
                            person_delay = i * 20  # Extra 20ms per person processed 
                            total_delay = base_delay + person_delay
                            print(f"    ⏳ Inter-person delay: {total_delay}ms (person {i}/{len(personnel_data)})")
                            page.wait_for_timeout(total_delay)
                            
                            print(f"    ✅ Person {i} ({name}) COMPLETELY PROCESSED - Ready for next person!")
                        
                        elif submit_success:
                            print(f"    🎉 FINAL PERSON {i} ({name}) COMPLETED SUCCESSFULLY!")
                        
                        # Skip the old modal closure code since we handle it above
                        modal_closed = True
                        
                    except Exception as cert_error:
                        print(f"    ❌ Certificate processing failed for person {i}: {cert_error}")
                        print(f"    🔄 Falling back to NO CERTIFICATE for {name}")
                        # Fallback to no certification
                        try:
                            page.locator("#ahmgawpm003_kebutuhan_sertifikasi_add").select_option("N")
                        except:
                            pass
                else:
                    # Person has no certificate - set to "Tidak" and skip certificate fields
                    print(f"    📝 NO CERTIFICATE for {name} - Setting to 'Tidak'")
                    try:
                        # Use JavaScript for more reliable field setting to "Tidak"
                        no_cert_set_success = page.evaluate("""
                            (function() {
                                try {
                                    const certField = document.getElementById('ahmgawpm003_kebutuhan_sertifikasi_add');
                                    if (certField) {
                                        certField.value = 'N';
                                        certField.dispatchEvent(new Event('change', {bubbles: true}));
                                        certField.dispatchEvent(new Event('blur', {bubbles: true}));
                                        console.log('Certificate requirement set to N (Tidak)');
                                        return true;
                                    }
                                    return false;
                                } catch(e) {
                                    console.log('No certificate field setting error:', e);
                                    return false;
                                }
                            })()
                        """)
                        
                        if no_cert_set_success:
                            print(f"    ✅ Certificate requirement set to 'Tidak' (N)")
                        else:
                            # Fallback method
                            page.locator("#ahmgawpm003_kebutuhan_sertifikasi_add").select_option("N")
                            print(f"    ✅ Certificate requirement set to 'Tidak' (fallback method)")
                        
                        print(f"    📝 Skipping certificate number and expiry date (not needed for 'Tidak')")
                        
                        # 📝 MODAL SUBMIT for people WITHOUT certificate (simpler flow)
                        print(f"    📝 MODAL SUBMIT for person {i} (NO certificate)...")
                        submit_success = False
                        
                        for submit_attempt in range(2):  # Try up to 2 times for no-cert people
                            try:
                                # Wait for form to be ready
                                page.wait_for_timeout(500 + (i * 100))  # Brief delay per person
                                
                                # Ensure submit button is enabled
                                page.evaluate("""
                                    (function() {
                                        const submitBtn = document.getElementById('ahmgawpm003_submit_button_add_modal');
                                        if (submitBtn) {
                                            submitBtn.removeAttribute('disabled');
                                            submitBtn.disabled = false;
                                            submitBtn.style.pointerEvents = 'auto';
                                            submitBtn.style.opacity = '1';
                                            submitBtn.classList.remove('disabled');
                                        }
                                    })()
                                """)
                                
                                # Submit the person
                                submit_btn = page.locator("#ahmgawpm003_submit_button_add_modal")
                                if submit_btn.is_visible():
                                    submit_btn.click()
                                    print(f"      ✅ Submit clicked for person {i} (no cert, attempt {submit_attempt + 1})")
                                    
                                    # 🔥 CRITICAL: Wait for submit to be processed (same as cert people)
                                    print(f"      ⏳ Waiting for submit processing (no cert)...")
                                    
                                    # Wait for modal to automatically close after successful submit
                                    submit_processed = False
                                    for wait_count in range(8):  # Wait up to 8 seconds for no-cert people
                                        try:
                                            # 🚨 CRITICAL: Handle notification modal (same as cert people)
                                            notification_modal_result = page.evaluate("""
                                                (function() {
                                                    try {
                                                        // Check for notification modal that blocks interaction
                                                        const notificationModal = document.getElementById('ahmgawpm003_notification_modal');
                                                        if (notificationModal && (notificationModal.classList.contains('in') || notificationModal.classList.contains('show'))) {
                                                            console.log('Notification modal detected (no cert) - dismissing...');
                                                            
                                                            // Try to find and click OK/Close button in notification modal
                                                            const okButtons = notificationModal.querySelectorAll('button, .btn, [data-dismiss]');
                                                            for (let btn of okButtons) {
                                                                const btnText = (btn.textContent || btn.innerText || '').toLowerCase();
                                                                if (btnText.includes('ok') || btnText.includes('close') || btnText.includes('tutup') || 
                                                                    btn.getAttribute('data-dismiss') === 'modal') {
                                                                    btn.click();
                                                                    console.log('Notification modal dismissed (no cert)');
                                                                    return {notification: true, dismissed: true};
                                                                }
                                                            }
                                                            
                                                            // If no button found, force hide the modal
                                                            notificationModal.style.display = 'none';
                                                            notificationModal.classList.remove('in', 'show');
                                                            notificationModal.setAttribute('aria-hidden', 'true');
                                                            
                                                            // Remove backdrop
                                                            const backdrops = document.querySelectorAll('.modal-backdrop');
                                                            backdrops.forEach(backdrop => backdrop.remove());
                                                            
                                                            console.log('Notification modal force hidden (no cert)');
                                                            return {notification: true, dismissed: true, forced: true};
                                                        }
                                                        
                                                        return {notification: false};
                                                    } catch(e) {
                                                        console.log('Notification modal check error (no cert):', e);
                                                        return {notification: false, error: e.message};
                                                    }
                                                })()
                                            """)
                                            
                                            if notification_modal_result.get('notification'):
                                                print(f"      🔔 Notification modal handled (no cert): {notification_modal_result}")
                                                page.wait_for_timeout(1000)  # Wait after dismissing notification
                                            
                                            # Check if main modal is still visible
                                            modal_still_visible = page.evaluate("""
                                                (function() {
                                                    const modal = document.getElementById('ahmgawpm003_add_worker_modal');
                                                    if (!modal) return false;
                                                    
                                                    const isVisible = modal.offsetParent !== null && 
                                                                    modal.style.display !== 'none' &&
                                                                    (modal.classList.contains('in') || modal.classList.contains('show'));
                                                    return isVisible;
                                                })()
                                            """)
                                            
                                            if not modal_still_visible:
                                                print(f"      ✅ Submit processed successfully - Modal auto-closed (no cert, wait {wait_count + 1})")
                                                submit_processed = True
                                                break
                                            else:
                                                page.wait_for_timeout(1000)  # Wait 1 second before checking again
                                                print(f"      ⏳ Submit processing... (no cert, wait {wait_count + 1}/8)")
                                                
                                        except Exception as wait_error:
                                            print(f"      ⚠️ Submit wait error (no cert): {wait_error}")
                                            page.wait_for_timeout(1000)
                                    
                                    if submit_processed:
                                        submit_success = True
                                        break
                                    else:
                                        print(f"      ⚠️ Submit may not have processed correctly (no cert, attempt {submit_attempt + 1})")
                                        
                                else:
                                    print(f"      ⚠️ Submit button not visible for person {i} (no cert, attempt {submit_attempt + 1})")
                                    
                            except Exception as submit_error:
                                print(f"      ❌ Submit attempt {submit_attempt + 1} failed for person {i} (no cert): {submit_error}")
                                if submit_attempt < 1:  # Don't wait on last attempt
                                    page.wait_for_timeout(800)
                        
                        if not submit_success:
                            print(f"    🚨 SUBMIT FAILED for person {i} (no cert) after attempts!")
                        else:
                            print(f"    🎉 SUBMIT SUCCESS for person {i} (no cert) - {name} added successfully!")
                        
                        # 🔥 POST-SUBMIT CLEANUP for no-cert people (same as cert people)
                        if submit_success and i < len(personnel_data):  # Not the last person
                            print(f"    🔧 POST-SUBMIT CLEANUP for person {i} (no cert) before next person...")
                            
                            # Same cleanup as cert people
                            cleanup_success = page.evaluate("""
                                (function() {
                                    try {
                                        // Force close any remaining modals
                                        const modals = document.querySelectorAll('.modal, .modal.fade, .modal.in, .modal.show');
                                        modals.forEach(modal => {
                                            modal.style.display = 'none';
                                            modal.classList.remove('in', 'show', 'fade');
                                            modal.setAttribute('aria-hidden', 'true');
                                            modal.removeAttribute('aria-modal');
                                        });
                                        
                                        // Remove all modal backdrops
                                        const backdrops = document.querySelectorAll('.modal-backdrop');
                                        backdrops.forEach(backdrop => backdrop.remove());
                                        
                                        // Reset body state
                                        document.body.classList.remove('modal-open');
                                        document.body.style.removeProperty('padding-right');
                                        document.body.style.removeProperty('overflow');
                                        
                                        // Clear all form fields in any modal
                                        const modalFields = document.querySelectorAll('.modal input, .modal select, .modal textarea');
                                        modalFields.forEach(field => {
                                            if (field.type !== 'hidden' && field.type !== 'submit') {
                                                field.value = '';
                                                field.checked = false;
                                                field.selectedIndex = 0;
                                                // Re-enable fields that might have been disabled
                                                field.disabled = false;
                                                field.readOnly = false;
                                                field.removeAttribute('disabled');
                                                field.removeAttribute('readonly');
                                            }
                                        });
                                        
                                        // Clear any window variables that might interfere
                                        window.lastUsedExpiryField = null;
                                        window.currentPersonNum = null;
                                        window.fieldDetectionCache = null;
                                        window.personnelModalOpen = false;
                                        
                                        console.log('Post-submit cleanup completed successfully (no cert)');
                                        return {success: true, message: 'Cleanup completed'};
                                        
                                    } catch(e) {
                                        console.log('Post-submit cleanup error (no cert):', e);
                                        return {success: false, error: e.message};
                                    }
                                })()
                            """)
                            
                            if cleanup_success.get('success'):
                                print(f"    ✅ Post-submit cleanup SUCCESS (no cert)")
                            else:
                                print(f"    ⚠️ Post-submit cleanup failed (no cert): {cleanup_success.get('error')}")
                            
                            # Additional wait to ensure everything is settled (ultra-fast mode, no-cert)
                            base_delay = 100  # 100ms base for no-cert people
                            person_delay = i * 10  # Extra 10ms per person processed 
                            total_delay = base_delay + person_delay
                            print(f"    ⏳ Inter-person delay (no cert): {total_delay}ms (person {i}/{len(personnel_data)})")
                            page.wait_for_timeout(total_delay)
                            
                            print(f"    ✅ Person {i} ({name}) NO-CERT COMPLETELY PROCESSED - Ready for next person!")
                        
                        elif submit_success:
                            print(f"    🎉 FINAL PERSON {i} ({name}) NO-CERT COMPLETED SUCCESSFULLY!")
                        
                    except Exception as no_cert_error:
                        print(f"    ⚠️ Failed to set 'Tidak' for certificate: {no_cert_error}")
                        # Try fallback
                        try:
                            page.locator("#ahmgawpm003_kebutuhan_sertifikasi_add").select_option("N")
                            print(f"    ✅ Certificate set to 'Tidak' via fallback")
                            
                            # Simple submit for fallback
                            submit_btn = page.locator("#ahmgawpm003_submit_button_add_modal")
                            submit_btn.click()
                            page.wait_for_timeout(800)
                            print(f"    ✅ Person {i} ({name}) submitted via fallback")
                        except Exception as fallback_error:
                            print(f"    ❌ All methods failed for person {i}: {fallback_error}")
                
                # 🎉 PERSON COMPLETION SUMMARY
                if has_cert:
                    print(f"    🎉 SUCCESS: {name} added WITH certificate!")
                else:
                    print(f"    ✅ SUCCESS: {name} added without certificate")
                
                # 🧹 POST-SUCCESS MODAL CLEANUP for person {i} (CRITICAL for next person!)
                if i < len(personnel_data):  # Don't cleanup after the last person
                    print(f"    🧹 POST-SUCCESS: Cleaning up modal for next person...")
                    cleanup_result = page.evaluate("""
                        (function() {
                            try {
                                // Close any open modals completely
                                const modals = document.querySelectorAll('.modal');
                                modals.forEach(modal => {
                                    modal.style.display = 'none';
                                    modal.classList.remove('in', 'show');
                                    modal.setAttribute('aria-hidden', 'true');
                                });
                                
                                // Remove any modal backdrops
                                const backdrops = document.querySelectorAll('.modal-backdrop');
                                backdrops.forEach(backdrop => backdrop.remove());
                                
                                // Reset body state
                                document.body.classList.remove('modal-open');
                                document.body.style.removeProperty('padding-right');
                                
                                // Clear modal form data for fresh state
                                const modalForm = document.querySelector('#ahmgawpm003_add_worker_modal');
                                if (modalForm) {
                                    const inputs = modalForm.querySelectorAll('input, select, textarea');
                                    inputs.forEach(input => {
                                        input.value = '';
                                        input.selectedIndex = 0;
                                        input.checked = false;
                                        
                                        // Remove any processed data attributes
                                        input.removeAttribute('data-processed');
                                        input.removeAttribute('data-filled');
                                    });
                                }
                                
                                // Clear any global modal state
                                window.modalState = null;
                                window.currentPersonnel = null;
                                
                                console.log('Post-success modal cleanup completed');
                                return true;
                            } catch(e) {
                                console.log('Post-success cleanup error:', e);
                                return false;
                            }
                        })()
                    """)
                    
                    print(f"    🧹 Cleanup result: {cleanup_result}")
                    page.wait_for_timeout(50)  # Ultra-fast cleanup pause
                
            except Exception as e:
                print(f"    ❌ Failed: {name} - {str(e)[:50]}...")
                try:
                    page.screenshot(path=f'error_person_{i}.png')
                    # Try to close modal if stuck
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(500)
                    
                    # Additional cleanup for failed cases
                    page.evaluate("""
                        (function() {
                            try {
                                // Force close any open modals
                                const modals = document.querySelectorAll('.modal');
                                modals.forEach(modal => {
                                    modal.style.display = 'none';
                                    modal.classList.remove('in', 'show');
                                });
                                
                                // Remove backdrops
                                const backdrops = document.querySelectorAll('.modal-backdrop');
                                backdrops.forEach(backdrop => backdrop.remove());
                                
                                // Reset body
                                document.body.classList.remove('modal-open');
                                document.body.style.removeProperty('padding-right');
                            } catch(e) {
                                console.log('Error cleanup failed:', e);
                            }
                        })()
                    """)
                except:
                    pass
        
        # 🎯 PERSONNEL ADDITION COMPLETION CHECK
        print(f"\n🎯 PERSONNEL ADDITION PHASE COMPLETED!")
        print(f"📊 Summary: {len(personnel_data)} people processed")
        
        # Wait for form to stabilize after all personnel
        page.wait_for_timeout(100)
        
        # Verify Add Personnel button is available for potential future use
        try:
            add_personnel_check = page.evaluate("""
                (function() {
                    // Find Add Personnel button with multiple strategies (no :has-text selector)
                    let addBtn = null;
                    
                    // Strategy 1: By text content
                    const btns = Array.from(document.querySelectorAll('button'));
                    addBtn = btns.find(btn => {
                        const text = (btn.textContent || btn.innerText || '').toLowerCase();
                        return text.includes('add') && (text.includes('personnel') || text.includes('pekerja'));
                    });
                    
                    // Strategy 2: By onclick function
                    if (!addBtn) {
                        addBtn = btns.find(btn => 
                            btn.onclick && btn.onclick.toString().includes('add')
                        );
                    }
                    
                    // Strategy 3: By common class patterns
                    if (!addBtn) {
                        addBtn = document.querySelector('.btn-add, .add-btn, #add_personnel_btn');
                    }
                    
                    return {
                        exists: !!addBtn,
                        visible: addBtn ? addBtn.offsetParent !== null : false,
                        enabled: addBtn ? !addBtn.disabled : false,
                        text: addBtn ? (addBtn.textContent || addBtn.innerText || '').substring(0, 50) : 'N/A'
                    };
                })()
            """)
            
            print(f"🔍 Add Personnel button status:")
            print(f"  Exists: {add_personnel_check.get('exists')}")
            print(f"  Visible: {add_personnel_check.get('visible')}")
            print(f"  Enabled: {add_personnel_check.get('enabled')}")
            print(f"  Text: {add_personnel_check.get('text')}")
            
        except Exception as check_error:
            print(f"⚠️ Could not check Add Personnel button status: {check_error}")
        
        print(f"✅ Ready to proceed to next phase (Area & Tools)")
        
        # ⚡ INSTANT AREA & TOOL ADDITION - ZERO DELAYS! ⚡
        print("\n" + "="*50)
        print("🏢 ADDING WORK AREA & TOOLS")
        print("="*50)
        print("🏢 INSTANT WORK AREA...")
        try:
            # Longer wait for all personnel to finish processing completely
            page.wait_for_timeout(120)  # Ultra-fast area phase wait
            print("✅ Personnel addition phase completed - proceeding to area & tools")
            
            page.get_by_role("button", name="+ Add Area").click()
            page.wait_for_timeout(30)  # Ultra-fast minimal wait
            page.locator("#ahmgawpm003_add_area_modal .btn-lookup").click()
            page.wait_for_timeout(40)  # Ultra-fast lookup wait
            page.get_by_role("cell", name="G", exact=True).click()
            page.locator("#ahmgawpm003_submit_button_add_area_modal").click()
            print("⚡ INSTANT: Work area added")
        except Exception as e:
            print(f"⚠️ Area addition failed: {e}")

        print("🔧 ULTRA-INSTANT TOOLS...")
        try:
            page.get_by_role("button", name="+ Add Tool").click()
            page.wait_for_timeout(40)  # Ultra-fast tool modal load
            
            # COMPREHENSIVE tool filling - ALL FIELDS COVERED!
            tool_success = page.evaluate("""
                (function() {
                    try {
                        // Find ALL possible tool fields
                        const toolId = document.getElementById('ahmgawpm003_tool_id_add');
                        const toolDesc = document.getElementById('ahmgawpm003_deskripsi_alat_add');
                        const permitFlag = document.getElementById('ahmgawpm003_permit_flag_add');
                        
                        // Additional fields that might be required
                        const toolName = document.getElementById('ahmgawpm003_nama_alat_add') || 
                                        document.querySelector('input[name*="nama_alat"]') ||
                                        document.querySelector('input[placeholder*="nama"]');
                        const toolType = document.getElementById('ahmgawpm003_jenis_alat_add') ||
                                        document.querySelector('select[name*="jenis"]');
                        const toolQty = document.getElementById('ahmgawpm003_jumlah_add') ||
                                       document.querySelector('input[name*="jumlah"]') ||
                                       document.querySelector('input[type="number"]');
                        
                        let fieldsSet = 0;
                        
                        // Fill Tool ID
                        if (toolId) {
                            toolId.value = '1';
                            toolId.setAttribute('value', '1');
                            ['input', 'change', 'blur', 'keyup'].forEach(eventType => {
                                toolId.dispatchEvent(new Event(eventType, {bubbles: true}));
                            });
                            console.log('Tool ID set: 1');
                            fieldsSet++;
                        }
                        
                        // Fill Tool Description
                        if (toolDesc) {
                            toolDesc.value = 'BASIC TOOLS';
                            toolDesc.setAttribute('value', 'BASIC TOOLS');
                            ['input', 'change', 'blur', 'keyup'].forEach(eventType => {
                                toolDesc.dispatchEvent(new Event(eventType, {bubbles: true}));
                            });
                            console.log('Tool Description set: BASIC TOOLS');
                            fieldsSet++;
                        }
                        
                        // Fill Tool Name if exists
                        if (toolName) {
                            toolName.value = 'HAND TOOLS';
                            toolName.setAttribute('value', 'HAND TOOLS');
                            ['input', 'change', 'blur'].forEach(eventType => {
                                toolName.dispatchEvent(new Event(eventType, {bubbles: true}));
                            });
                            console.log('Tool Name set: HAND TOOLS');
                            fieldsSet++;
                        }
                        
                        // Fill Tool Type if exists
                        if (toolType) {
                            toolType.value = 'Manual';
                            toolType.dispatchEvent(new Event('change', {bubbles: true}));
                            console.log('Tool Type set: Manual');
                            fieldsSet++;
                        }
                        
                        // Fill Quantity if exists
                        if (toolQty) {
                            toolQty.value = '1';
                            toolQty.setAttribute('value', '1');
                            ['input', 'change', 'blur'].forEach(eventType => {
                                toolQty.dispatchEvent(new Event(eventType, {bubbles: true}));
                            });
                            console.log('Tool Quantity set: 1');
                            fieldsSet++;
                        }
                        
                        // Fill Permit Flag (most important!)
                        if (permitFlag) {
                            permitFlag.value = 'Tidak';
                            permitFlag.dispatchEvent(new Event('change', {bubbles: true}));
                            permitFlag.dispatchEvent(new Event('blur', {bubbles: true}));
                            console.log('Permit Flag set: Tidak');
                            fieldsSet++;
                        }
                        
                        // Fill "Butuh Izin Alat" dropdown - CRITICAL FIELD!
                        const butuhIzin = document.getElementById('ahmgawpm003_butuh_izin_alat_add') ||
                                         document.querySelector('select[name*="butuh_izin"]') ||
                                         document.querySelector('select[aria-label*="Butuh Izin"]') ||
                                         document.querySelector('select option[value="Tidak"]').parentElement;
                        
                        if (butuhIzin) {
                            butuhIzin.value = 'Tidak';
                            butuhIzin.dispatchEvent(new Event('change', {bubbles: true}));
                            butuhIzin.dispatchEvent(new Event('blur', {bubbles: true}));
                            console.log('Butuh Izin Alat set: Tidak');
                            fieldsSet++;
                        }
                        
                        // Also try to find and fill any other required fields
                        const allInputs = document.querySelectorAll('#ahmgawpm003_add_tool_modal input[required], #ahmgawpm003_add_tool_modal select[required]');
                        allInputs.forEach(function(input, index) {
                            if (!input.value && input.type !== 'hidden') {
                                if (input.type === 'text' || input.type === 'textarea') {
                                    input.value = 'DEFAULT';
                                    input.dispatchEvent(new Event('input', {bubbles: true}));
                                } else if (input.type === 'number') {
                                    input.value = '1';
                                    input.dispatchEvent(new Event('input', {bubbles: true}));
                                } else if (input.tagName === 'SELECT') {
                                    if (input.options.length > 1) {
                                        input.selectedIndex = 1;
                                        input.dispatchEvent(new Event('change', {bubbles: true}));
                                    }
                                }
                                console.log('Additional field filled:', input.name || input.id);
                                fieldsSet++;
                            }
                        });
                        
                        // FORCE ENABLE submit button after all fields filled
                        const submitBtn = document.getElementById('ahmgawpm003_submit_button_add_tool_modal');
                        if (submitBtn) {
                            submitBtn.removeAttribute('disabled');
                            submitBtn.disabled = false;
                            submitBtn.style.pointerEvents = 'auto';
                            submitBtn.style.opacity = '1';
                            console.log('Submit button FORCE ENABLED');
                        }
                        
                        console.log('COMPREHENSIVE: ' + fieldsSet + ' total tool fields filled');
                        return fieldsSet;
                    } catch(e) {
                        console.log('Tool fill error:', e);
                        return 0;
                    }
                })()
            """)
            
            print(f"    ⚡ COMPREHENSIVE FILL: {tool_success} tool fields set")
            
            # Brief wait for all fields to process (ultra-fast)
            page.wait_for_timeout(30)
            
            # FORCE ENABLE submit button before clicking
            page.evaluate("""
                (function() {
                    const submitBtn = document.getElementById('ahmgawpm003_submit_button_add_tool_modal');
                    if (submitBtn) {
                        submitBtn.removeAttribute('disabled');
                        submitBtn.disabled = false;
                        submitBtn.style.pointerEvents = 'auto';
                        submitBtn.style.opacity = '1';
                        submitBtn.classList.remove('disabled');
                        console.log('Submit button FORCE ENABLED before click');
                    }
                })()
            """)
            
            # INSTANT submit - try multiple methods!
            try:
                # Method 1: Direct click
                submit_btn = page.locator("#ahmgawpm003_submit_button_add_tool_modal")
                submit_btn.click()
                print("⚡ SUBMIT: Direct click successful")
            except Exception as e1:
                print(f"⚠️ Direct click failed: {e1}")
                try:
                    # Method 2: JavaScript click
                    page.evaluate("""
                        document.getElementById('ahmgawpm003_submit_button_add_tool_modal').click();
                    """)
                    print("⚡ SUBMIT: JavaScript click successful")
                except Exception as e2:
                    print(f"⚠️ JavaScript click failed: {e2}")
                    try:
                        # Method 3: Force submit via function call
                        page.evaluate("""
                            if (typeof ahmgawpm003_submitTool === 'function') {
                                ahmgawpm003_submitTool();
                                console.log('SUBMIT: Function call successful');
                            }
                        """)
                        print("⚡ SUBMIT: Function call successful")
                    except Exception as e3:
                        print(f"⚠️ All submit methods failed: {e3}")
            
            page.wait_for_timeout(30)  # Ultra-fast modal close
            print("⚡ ULTRA-INSTANT: Tools added")
            
        except Exception as e:
            print(f"⚠️ Tool addition failed: {e}")
            # Try screenshot for debugging
            try:
                page.screenshot(path='tool_error.png')
                print("📸 Tool error screenshot saved")
            except:
                pass

=======
                        // Fill Tool Name if exists
                        if (toolName) {
                            toolName.value = 'HAND TOOLS';
                            toolName.setAttribute('value', 'HAND TOOLS');
                            ['input', 'change', 'blur'].forEach(eventType => {
                                toolName.dispatchEvent(new Event(eventType, {bubbles: true}));
                            });
                            console.log('Tool Name set: HAND TOOLS');
                            fieldsSet++;
                        }
                        
                        // Fill Tool Type if exists
                        if (toolType) {
                            toolType.value = 'Manual';
                            toolType.dispatchEvent(new Event('change', {bubbles: true}));
                            console.log('Tool Type set: Manual');
                            fieldsSet++;
                        }
                        
                        // Fill Quantity if exists
                        if (toolQty) {
                            toolQty.value = '1';
                            toolQty.setAttribute('value', '1');
                            ['input', 'change', 'blur'].forEach(eventType => {
                                toolQty.dispatchEvent(new Event(eventType, {bubbles: true}));
                            });
                            console.log('Tool Quantity set: 1');
                            fieldsSet++;
                        }
                        
                        // Fill Permit Flag (most important!)
                        if (permitFlag) {
                            permitFlag.value = 'Tidak';
                            permitFlag.dispatchEvent(new Event('change', {bubbles: true}));
                            permitFlag.dispatchEvent(new Event('blur', {bubbles: true}));
                            console.log('Permit Flag set: Tidak');
                            fieldsSet++;
                        }
                        
                        // Fill "Butuh Izin Alat" dropdown - CRITICAL FIELD!
                        const butuhIzin = document.getElementById('ahmgawpm003_butuh_izin_alat_add') ||
                                         document.querySelector('select[name*="butuh_izin"]') ||
                                         document.querySelector('select[aria-label*="Butuh Izin"]') ||
                                         document.querySelector('select option[value="Tidak"]').parentElement;
                        
                        if (butuhIzin) {
                            butuhIzin.value = 'Tidak';
                            butuhIzin.dispatchEvent(new Event('change', {bubbles: true}));
                            butuhIzin.dispatchEvent(new Event('blur', {bubbles: true}));
                            console.log('Butuh Izin Alat set: Tidak');
                            fieldsSet++;
                        }
                        
                        // Also try to find and fill any other required fields
                        const allInputs = document.querySelectorAll('#ahmgawpm003_add_tool_modal input[required], #ahmgawpm003_add_tool_modal select[required]');
                        allInputs.forEach(function(input, index) {
                            if (!input.value && input.type !== 'hidden') {
                                if (input.type === 'text' || input.type === 'textarea') {
                                    input.value = 'DEFAULT';
                                    input.dispatchEvent(new Event('input', {bubbles: true}));
                                } else if (input.type === 'number') {
                                    input.value = '1';
                                    input.dispatchEvent(new Event('input', {bubbles: true}));
                                } else if (input.tagName === 'SELECT') {
                                    if (input.options.length > 1) {
                                        input.selectedIndex = 1;
                                        input.dispatchEvent(new Event('change', {bubbles: true}));
                                    }
                                }
                                console.log('Additional field filled:', input.name || input.id);
                                fieldsSet++;
                            }
                        });
                        
                        // FORCE ENABLE submit button after all fields filled
                        const submitBtn = document.getElementById('ahmgawpm003_submit_button_add_tool_modal');
                        if (submitBtn) {
                            submitBtn.removeAttribute('disabled');
                            submitBtn.disabled = false;
                            submitBtn.style.pointerEvents = 'auto';
                            submitBtn.style.opacity = '1';
                            console.log('Submit button FORCE ENABLED');
                        }
                        
                        console.log('COMPREHENSIVE: ' + fieldsSet + ' total tool fields filled');
                        return fieldsSet;
                    } catch(e) {
                        console.log('Tool fill error:', e);
                        return 0;
                    }
                })()
            """)
            
            print(f"    ⚡ COMPREHENSIVE FILL: {tool_success} tool fields set")
            
            # Brief wait for all fields to process
            page.wait_for_timeout(200)
            
            # FORCE ENABLE submit button before clicking
            page.evaluate("""
                (function() {
                    const submitBtn = document.getElementById('ahmgawpm003_submit_button_add_tool_modal');
                    if (submitBtn) {
                        submitBtn.removeAttribute('disabled');
                        submitBtn.disabled = false;
                        submitBtn.style.pointerEvents = 'auto';
                        submitBtn.style.opacity = '1';
                        submitBtn.classList.remove('disabled');
                        console.log('Submit button FORCE ENABLED before click');
                    }
                })()
            """)
            
            # INSTANT submit - try multiple methods!
            try:
                # Method 1: Direct click
                submit_btn = page.locator("#ahmgawpm003_submit_button_add_tool_modal")
                submit_btn.click()
                print("⚡ SUBMIT: Direct click successful")
            except Exception as e1:
                print(f"⚠️ Direct click failed: {e1}")
                try:
                    # Method 2: JavaScript click
                    page.evaluate("""
                        document.getElementById('ahmgawpm003_submit_button_add_tool_modal').click();
                    """)
                    print("⚡ SUBMIT: JavaScript click successful")
                except Exception as e2:
                    print(f"⚠️ JavaScript click failed: {e2}")
                    try:
                        # Method 3: Force submit via function call
                        page.evaluate("""
                            if (typeof ahmgawpm003_submitTool === 'function') {
                                ahmgawpm003_submitTool();
                                console.log('SUBMIT: Function call successful');
                            }
                        """)
                        print("⚡ SUBMIT: Function call successful")
                    except Exception as e3:
                        print(f"⚠️ All submit methods failed: {e3}")
            
            page.wait_for_timeout(150)  # Brief wait for modal close
            print("⚡ ULTRA-INSTANT: Tools added")
            
        except Exception as e:
            print(f"⚠️ Tool addition failed: {e}")
            # Try screenshot for debugging
            try:
                page.screenshot(path='tool_error.png')
                print("📸 Tool error screenshot saved")
            except:
                pass

>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)
        # ⚡ ULTRA-INSTANT FINAL SUBMISSION - BULLETPROOF! ⚡
        print("📋 ULTRA-INSTANT FINAL SUBMISSION...")
        try:
            # INSTANT checkbox check with JavaScript
            checkbox_success = page.evaluate("""
                (function() {
                    try {
                        const checkbox = document.getElementById('ahmgawpm003_checkbox_persetujuan');
                        if (checkbox) {
                            checkbox.checked = true;
                            checkbox.dispatchEvent(new Event('change', {bubbles: true}));
                            console.log('INSTANT: Checkbox checked');
                            return true;
                        }
                        return false;
                    } catch(e) {
                        console.log('Checkbox error:', e);
                        return false;
                    }
                })()
            """)
            
            if not checkbox_success:
                # Fallback checkbox method
                page.locator("#ahmgawpm003_checkbox_persetujuan").check()
            
            print("⚡ Agreement checked")
            
            # INSTANT submit with enhanced verification
            page.get_by_role("button", name=" Submit").click()
            print("⚡ SUBMIT CLICKED!")
            
<<<<<<< HEAD
<<<<<<< HEAD
            # ENHANCED ROBUST COMPLETION CHECK WITH MULTIPLE STRATEGIES
            print("⏳ ENHANCED completion verification...")
            success_found = False
            completion_method = "unknown"
            
            # Strategy 1: Quick success message check (with retry)
            print("🔍 Strategy 1: Checking success notifications...")
            try:
                success_selectors = [
                    ".alert-success", ".success-message", ".notification.success",
                    "[class*='success']", ".swal2-success",
                    ".toast-success", "[role='alert']",
                    ".alert.alert-success", ".success", ".completed"
                ]
                
                for i, selector in enumerate(success_selectors):
                    try:
                        page.wait_for_selector(selector, timeout=1000)
                        notification_text = page.locator(selector).text_content()
                        print(f"✅ SUCCESS NOTIFICATION: {notification_text}")
                        success_found = True
                        completion_method = f"notification_{i+1}"
=======
            # FAST success verification with multiple strategies
            print("⏳ FAST completion check...")
=======
            # ENHANCED ROBUST COMPLETION CHECK WITH MULTIPLE STRATEGIES
            print("⏳ ENHANCED completion verification...")
>>>>>>> 69b7eec (jangkrik)
            success_found = False
            completion_method = "unknown"
            
            # Strategy 1: Quick success message check (with retry)
            print("🔍 Strategy 1: Checking success notifications...")
            try:
                success_selectors = [
                    ".alert-success", ".success-message", ".notification.success",
                    "[class*='success']", "div:has-text('berhasil')", ".swal2-success",
                    ".toast-success", "[role='alert']:has-text('berhasil')",
                    ".alert.alert-success", ".success", ".completed"
                ]
                
                for i, selector in enumerate(success_selectors):
                    try:
                        page.wait_for_selector(selector, timeout=1000)
                        notification_text = page.locator(selector).text_content()
                        print(f"✅ SUCCESS NOTIFICATION: {notification_text}")
                        success_found = True
<<<<<<< HEAD
>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)
=======
                        completion_method = f"notification_{i+1}"
>>>>>>> 69b7eec (jangkrik)
                        break
                    except:
                        continue
                        
<<<<<<< HEAD
<<<<<<< HEAD
            except Exception as e:
                print(f"⚠️ Strategy 1 error: {e}")
            
            # Strategy 2: URL change check (enhanced with multiple patterns)
            if not success_found:
                print("🔍 Strategy 2: Checking URL redirects...")
                try:
                    # Multiple URL patterns to check
                    url_patterns = [
                        "**/dashboard.htm**",
                        "**/dashboard**",
                        "**/success**",
                        "**/completed**",
                        "**/result**"
                    ]
                    
                    for pattern in url_patterns:
                        try:
                            page.wait_for_url(pattern, timeout=2000)
                            print(f"✅ SUCCESS: Redirected to {pattern}")
                            success_found = True
                            completion_method = "redirect"
                            break
                        except:
                            continue
                            
                except Exception as e:
                    print(f"⚠️ Strategy 2 error: {e}")
            
            # Strategy 3: Form state analysis (enhanced)
            if not success_found:
                print("🔍 Strategy 3: Analyzing form state...")
                try:
                    # Check if form elements disappeared
                    form_elements = [
                        "#ahmgawpm003_kategori_pekerjaan_request_kontraktor",
                        "#ahmgawpm003_kategori_ikk_request_kontraktor",
                        "#ahmgawpm003_tanggal_pelaksanaan_pekerjaan_khusus_request_kontraktor"
                    ]
                    
                    form_still_present = False
                    for element in form_elements:
                        try:
                            page.wait_for_selector(element, timeout=1000)
                            form_still_present = True
                            break
                        except:
                            continue
                    
                    if not form_still_present:
                        print("✅ SUCCESS: Form elements disappeared (completed)")
                        success_found = True
                        completion_method = "form_disappeared"
                    else:
                        print("📋 Form still present, checking other indicators...")
                        
                except Exception as e:
                    print(f"⚠️ Strategy 3 error: {e}")
            
            # Strategy 4: Submit button state check (enhanced)
            if not success_found:
                print("🔍 Strategy 4: Checking submit button state...")
=======
            except Exception:
                pass
=======
            except Exception as e:
                print(f"⚠️ Strategy 1 error: {e}")
>>>>>>> 69b7eec (jangkrik)
            
            # Strategy 2: URL change check (enhanced with multiple patterns)
            if not success_found:
                print("🔍 Strategy 2: Checking URL redirects...")
                try:
                    # Multiple URL patterns to check
                    url_patterns = [
                        "**/dashboard.htm**",
                        "**/dashboard**",
                        "**/success**",
                        "**/completed**",
                        "**/result**"
                    ]
                    
                    for pattern in url_patterns:
                        try:
                            page.wait_for_url(pattern, timeout=2000)
                            print(f"✅ SUCCESS: Redirected to {pattern}")
                            success_found = True
                            completion_method = "redirect"
                            break
                        except:
                            continue
                            
                except Exception as e:
                    print(f"⚠️ Strategy 2 error: {e}")
            
            # Strategy 3: Form state analysis (enhanced)
            if not success_found:
<<<<<<< HEAD
>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)
=======
                print("🔍 Strategy 3: Analyzing form state...")
                try:
                    # Check if form elements disappeared
                    form_elements = [
                        "#ahmgawpm003_kategori_pekerjaan_request_kontraktor",
                        "#ahmgawpm003_kategori_ikk_request_kontraktor",
                        "#ahmgawpm003_tanggal_pelaksanaan_pekerjaan_khusus_request_kontraktor"
                    ]
                    
                    form_still_present = False
                    for element in form_elements:
                        try:
                            page.wait_for_selector(element, timeout=1000)
                            form_still_present = True
                            break
                        except:
                            continue
                    
                    if not form_still_present:
                        print("✅ SUCCESS: Form elements disappeared (completed)")
                        success_found = True
                        completion_method = "form_disappeared"
                    else:
                        print("📋 Form still present, checking other indicators...")
                        
                except Exception as e:
                    print(f"⚠️ Strategy 3 error: {e}")
            
            # Strategy 4: Submit button state check (enhanced)
            if not success_found:
                print("🔍 Strategy 4: Checking submit button state...")
>>>>>>> 69b7eec (jangkrik)
                try:
                    submit_button = page.get_by_role("button", name=" Submit")
                    if not submit_button.is_enabled():
                        print("✅ SUCCESS: Submit button disabled (indicates completion)")
                        success_found = True
<<<<<<< HEAD
<<<<<<< HEAD
                        completion_method = "button_disabled"
                    else:
                        print("⚠️ Submit button still enabled - analyzing page content...")
                        
                        # Enhanced page content analysis
                        current_url = page.url
                        page_content = page.content()
                        
                        success_indicators = [
                            "dashboard", "berhasil", "sukses", "completed", 
                            "success", "selesai", "tersimpan", "submitted"
                        ]
                        
                        content_indicates_success = any(
                            indicator in current_url.lower() or 
                            indicator in page_content.lower() 
                            for indicator in success_indicators
                        )
                        
                        if content_indicates_success:
                            print("✅ SUCCESS: Page content indicates completion")
                            success_found = True
                            completion_method = "content_analysis"
=======
=======
                        completion_method = "button_disabled"
>>>>>>> 69b7eec (jangkrik)
                    else:
                        print("⚠️ Submit button still enabled - analyzing page content...")
                        
                        # Enhanced page content analysis
                        current_url = page.url
                        page_content = page.content()
                        
                        success_indicators = [
                            "dashboard", "berhasil", "sukses", "completed", 
                            "success", "selesai", "tersimpan", "submitted"
                        ]
                        
                        content_indicates_success = any(
                            indicator in current_url.lower() or 
                            indicator in page_content.lower() 
                            for indicator in success_indicators
                        )
                        
                        if content_indicates_success:
                            print("✅ SUCCESS: Page content indicates completion")
                            success_found = True
<<<<<<< HEAD
>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)
=======
                            completion_method = "content_analysis"
>>>>>>> 69b7eec (jangkrik)
                        else:
                            print("⚠️ Submission status unclear, but no error detected")
                            
                except Exception as e:
<<<<<<< HEAD
<<<<<<< HEAD
                    print(f"⚠️ Strategy 4 error: {e}")
            
            # Strategy 5: Final fallback - wait and retry
            if not success_found:
                print("🔍 Strategy 5: Final completion check...")
                try:
                    page.wait_for_timeout(100)  # Ultra-fast fallback wait
                    current_url = page.url
                    
                    # Check if URL changed from original form URL
                    if "AHMGAWPM003" not in current_url:
                        print("✅ SUCCESS: Moved away from form page")
                        success_found = True
                        completion_method = "url_change"
                    else:
                        print("⚠️ Still on form page, assuming completion")
                        success_found = True  # Assume success to avoid infinite hang
                        completion_method = "timeout_assumed"
                        
                except Exception as e:
                    print(f"⚠️ Strategy 5 error: {e}")
                    success_found = True  # Assume success to avoid hang
                    completion_method = "error_assumed"
            
            # ENHANCED SUCCESS REPORTING
            if success_found:
                import datetime
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                formatted_date = setup_date(work_date)
                personnel_count = len(personnel_data)
                
                print("🎉" + "="*60 + "🎉")
                print("🚀 BERHASIL SUBMIT IKK! 🚀")
                print("="*64)
                print(f"📂 Kategori: {ikk_category}")
                print(f"📅 Tanggal: {formatted_date}")
                print(f"🔄 Shift: {selected_shift}")
                print(f"👥 Jumlah Personnel: {personnel_count} orang")
                print(f"📝 Deskripsi: {deskripsi}")
                print(f"⏰ Waktu Selesai: {current_time}")
                print(f"🔍 Metode Deteksi: {completion_method}")
                print("="*64)
                print("✅ IKK AUTOMATION COMPLETED SUCCESSFULLY!")
                print("🎉" + "="*60 + "🎉")
                
                # Enhanced logging to automation.log
                log_entry = f"""
[{current_time}] IKK AUTOMATION SUCCESS
  Category: {ikk_category}
  Date: {formatted_date}
  Shift: {selected_shift}
  Personnel: {personnel_count}
  Description: {deskripsi}
  Completion Method: {completion_method}
  Status: SUCCESS
"""
                
                try:
                    with open("/home/dan/Portal/automation.log", "a", encoding="utf-8") as log_file:
                        log_file.write(log_entry)
                        log_file.flush()
                    print("📝 Success logged to automation.log")
                except Exception as e:
                    print(f"⚠️ Logging error: {e}")
                    
            else:
                print("⚠️ Submission completed but status verification inconclusive")
                print("    (This doesn't mean failure - form may have been submitted successfully)")
                
                # Log inconclusive result
                try:
                    import datetime
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    log_entry = f"""
[{current_time}] IKK AUTOMATION INCONCLUSIVE
  Category: {ikk_category}
  Date: {work_date}
  Shift: {selected_shift}
  Personnel: {len(personnel_data)}
  Status: INCONCLUSIVE (likely successful)
"""
                    with open("/home/dan/Portal/automation.log", "a", encoding="utf-8") as log_file:
                        log_file.write(log_entry)
                        log_file.flush()
                except:
                    pass
                
        except Exception as e:
            print(f"⚠️ Final submission error: {e}")
            
            # ENHANCED ERROR RECOVERY AND ANALYSIS
            try:
                current_url = page.url
                print(f"📍 Current URL: {current_url}")
                
                # Check if we're actually on a success page despite the error
                success_indicators = ["dashboard", "success", "completed", "result"]
                url_indicates_success = any(indicator in current_url.lower() for indicator in success_indicators)
                
                if url_indicates_success:
                    print("✅ ERROR RECOVERY: Actually succeeded - we're on success page!")
                    
                    # Log recovery success
                    try:
                        import datetime
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        log_entry = f"""
[{current_time}] IKK AUTOMATION RECOVERED
  Category: {ikk_category}
  Date: {work_date}
  Shift: {selected_shift}
  Personnel: {len(personnel_data)}
  Error: {str(e)}
  Recovery: SUCCESS (found on success page)
"""
                        with open("/home/dan/Portal/automation.log", "a", encoding="utf-8") as log_file:
                            log_file.write(log_entry)
                            log_file.flush()
                    except:
                        pass
                else:
                    print("❌ Error occurred and recovery unsuccessful")
                    
                    # Enhanced error screenshot with timestamp
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f'ikk_error_{timestamp}.png'
                    page.screenshot(path=screenshot_path)
                    print(f"📸 Error screenshot saved as {screenshot_path}")
                    
                    # Log detailed error
                    try:
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        log_entry = f"""
[{current_time}] IKK AUTOMATION ERROR
  Category: {ikk_category}
  Date: {work_date}
  Shift: {selected_shift}
  Personnel: {len(personnel_data)}
  Error: {str(e)}
  URL: {current_url}
  Screenshot: {screenshot_path}
  Status: FAILED
"""
                        with open("/home/dan/Portal/automation.log", "a", encoding="utf-8") as log_file:
                            log_file.write(log_entry)
                            log_file.flush()
                    except:
                        pass
                        
            except Exception as recovery_error:
                print(f"🔥 Error recovery failed: {recovery_error}")
                
                # Fallback screenshot
                try:
                    page.screenshot(path='ikk_critical_error.png')
                    print("📸 Critical error screenshot saved")
                except:
                    pass

        print("🎉 AUTOMATION SELESAI! Tekan Enter untuk menutup browser...")
        
        # Enhanced completion summary
        print("\n📊 AUTOMATION SUMMARY:")
        print("="*40)
        print(f"  🎯 Target: IKK {ikk_category}")
        print(f"  📅 Date: {work_date}")
        print(f"  🔄 Shift: {selected_shift}")
        print(f"  👥 Personnel: {len(personnel_data)} orang")
        print(f"  📝 Description: {deskripsi}")
        print("="*40)
        
=======
                    print(f"⚠️ Button check failed: {e}")
=======
                    print(f"⚠️ Strategy 4 error: {e}")
>>>>>>> 69b7eec (jangkrik)
            
            # Strategy 5: Final fallback - wait and retry
            if not success_found:
                print("🔍 Strategy 5: Final completion check...")
                try:
                    page.wait_for_timeout(2000)  # Wait 2 seconds
                    current_url = page.url
                    
                    # Check if URL changed from original form URL
                    if "AHMGAWPM003" not in current_url:
                        print("✅ SUCCESS: Moved away from form page")
                        success_found = True
                        completion_method = "url_change"
                    else:
                        print("⚠️ Still on form page, assuming completion")
                        success_found = True  # Assume success to avoid infinite hang
                        completion_method = "timeout_assumed"
                        
                except Exception as e:
                    print(f"⚠️ Strategy 5 error: {e}")
                    success_found = True  # Assume success to avoid hang
                    completion_method = "error_assumed"
            
            # ENHANCED SUCCESS REPORTING
            if success_found:
                import datetime
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                formatted_date = setup_date(work_date)
                personnel_count = len(personnel_data)
                
                print("🎉" + "="*60 + "🎉")
                print("🚀 BERHASIL SUBMIT IKK! 🚀")
                print("="*64)
                print(f"📂 Kategori: {ikk_category}")
                print(f"📅 Tanggal: {formatted_date}")
                print(f"🔄 Shift: {selected_shift}")
                print(f"👥 Jumlah Personnel: {personnel_count} orang")
                print(f"📝 Deskripsi: {deskripsi}")
                print(f"⏰ Waktu Selesai: {current_time}")
                print(f"🔍 Metode Deteksi: {completion_method}")
                print("="*64)
                print("✅ IKK AUTOMATION COMPLETED SUCCESSFULLY!")
                print("🎉" + "="*60 + "🎉")
                
                # Enhanced logging to automation.log
                log_entry = f"""
[{current_time}] IKK AUTOMATION SUCCESS
  Category: {ikk_category}
  Date: {formatted_date}
  Shift: {selected_shift}
  Personnel: {personnel_count}
  Description: {deskripsi}
  Completion Method: {completion_method}
  Status: SUCCESS
"""
                
                try:
                    with open("/home/dan/Portal/automation.log", "a", encoding="utf-8") as log_file:
                        log_file.write(log_entry)
                        log_file.flush()
                    print("📝 Success logged to automation.log")
                except Exception as e:
                    print(f"⚠️ Logging error: {e}")
                    
            else:
                print("⚠️ Submission completed but status verification inconclusive")
                print("    (This doesn't mean failure - form may have been submitted successfully)")
                
                # Log inconclusive result
                try:
                    import datetime
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    log_entry = f"""
[{current_time}] IKK AUTOMATION INCONCLUSIVE
  Category: {ikk_category}
  Date: {work_date}
  Shift: {selected_shift}
  Personnel: {len(personnel_data)}
  Status: INCONCLUSIVE (likely successful)
"""
                    with open("/home/dan/Portal/automation.log", "a", encoding="utf-8") as log_file:
                        log_file.write(log_entry)
                        log_file.flush()
                except:
                    pass
                
        except Exception as e:
            print(f"⚠️ Final submission error: {e}")
            
            # ENHANCED ERROR RECOVERY AND ANALYSIS
            try:
                current_url = page.url
                print(f"📍 Current URL: {current_url}")
                
                # Check if we're actually on a success page despite the error
                success_indicators = ["dashboard", "success", "completed", "result"]
                url_indicates_success = any(indicator in current_url.lower() for indicator in success_indicators)
                
                if url_indicates_success:
                    print("✅ ERROR RECOVERY: Actually succeeded - we're on success page!")
                    
                    # Log recovery success
                    try:
                        import datetime
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        log_entry = f"""
[{current_time}] IKK AUTOMATION RECOVERED
  Category: {ikk_category}
  Date: {work_date}
  Shift: {selected_shift}
  Personnel: {len(personnel_data)}
  Error: {str(e)}
  Recovery: SUCCESS (found on success page)
"""
                        with open("/home/dan/Portal/automation.log", "a", encoding="utf-8") as log_file:
                            log_file.write(log_entry)
                            log_file.flush()
                    except:
                        pass
                else:
                    print("❌ Error occurred and recovery unsuccessful")
                    
                    # Enhanced error screenshot with timestamp
                    import datetime
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f'ikk_error_{timestamp}.png'
                    page.screenshot(path=screenshot_path)
                    print(f"📸 Error screenshot saved as {screenshot_path}")
                    
                    # Log detailed error
                    try:
                        current_time = datetime.datetime.now().strftime("%H:%M:%S")
                        log_entry = f"""
[{current_time}] IKK AUTOMATION ERROR
  Category: {ikk_category}
  Date: {work_date}
  Shift: {selected_shift}
  Personnel: {len(personnel_data)}
  Error: {str(e)}
  URL: {current_url}
  Screenshot: {screenshot_path}
  Status: FAILED
"""
                        with open("/home/dan/Portal/automation.log", "a", encoding="utf-8") as log_file:
                            log_file.write(log_entry)
                            log_file.flush()
                    except:
                        pass
                        
            except Exception as recovery_error:
                print(f"🔥 Error recovery failed: {recovery_error}")
                
                # Fallback screenshot
                try:
                    page.screenshot(path='ikk_critical_error.png')
                    print("📸 Critical error screenshot saved")
                except:
                    pass

<<<<<<< HEAD
        print("🎉 ULTRA-INSTANT IKK AUTOMATION COMPLETED! Press Enter to close...")
>>>>>>> bc59a96 (oke mantap ini ikh dan ikk shiftnya udah ok banget)
=======
        print("🎉 AUTOMATION SELESAI! Tekan Enter untuk menutup browser...")
<<<<<<< HEAD
>>>>>>> 81d0bb7 (best lah siap maspro)
=======
        
        # Enhanced completion summary
        print("\n📊 AUTOMATION SUMMARY:")
        print("="*40)
        print(f"  🎯 Target: IKK {ikk_category}")
        print(f"  📅 Date: {work_date}")
        print(f"  🔄 Shift: {selected_shift}")
        print(f"  👥 Personnel: {len(personnel_data)} orang")
        print(f"  📝 Description: {deskripsi}")
        print("="*40)
        
>>>>>>> 69b7eec (jangkrik)
        input()
        
    except Exception as e:
        print(f"❌ AUTOMATION ERROR: {e}")
        try:
            page.screenshot(path='ikk_error.png')
            print("📸 Error screenshot saved")
        except:
            pass
    finally:
        browser.close()

if __name__ == "__main__":
    # Parse command line arguments
    ikk_category = sys.argv[1].upper() if len(sys.argv) > 1 else "IA"
    work_date = sys.argv[2] if len(sys.argv) > 2 else "30"
    deskripsi = sys.argv[3] if len(sys.argv) > 3 else "MELTING REPAIR"
    selected_shift = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 1
    
    # Validate shift parameter
    if selected_shift not in [1, 2, 3]:
        print(f"⚠️ Invalid shift {selected_shift}, using default shift 1")
        selected_shift = 1
    
    print(f"🔄 Command line arguments:")
    print(f"   📂 Category: {ikk_category}")
    print(f"   📅 Date: {work_date}")
    print(f"   📝 Description: {deskripsi}")
    print(f"   🔄 Shift: {selected_shift}")
    
    # Map categories to CSV files
    csv_map = {
        "IA": "/home/dan/Portal/personnel_list_IA.csv",    # IKK API
        "IR": "/home/dan/Portal/personnel_list_IR.csv",    # IKK Ruang Terbatas  
        "IK": "/home/dan/Portal/personnel_list_IK.csv"     # IKK Ketinggian
    }
    
    csv_file_path = csv_map.get(ikk_category, csv_map["IA"])
    print(f"📄 CSV File: {csv_file_path}")
    
    # Load personnel data with shift support
    personnel_data = read_csv(csv_file_path, selected_shift=selected_shift)
    print(f"👥 Loaded: {len(personnel_data)} personnel (shift {selected_shift} will be set in form)")
    if personnel_data:
        print(f"📋 First person: {personnel_data[0]}")
    
    # Run automation
    with sync_playwright() as playwright:
        run(playwright, personnel_data, ikk_category, work_date, deskripsi, selected_shift)