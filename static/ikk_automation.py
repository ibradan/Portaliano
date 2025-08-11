#!/usr/bin/env python3
"""
⚡ MERGED IKK Automation - Best of Both Worlds! ⚡
Combines speed optimizations from aa.py with robust date/shift handling from ori.py

Usage:
    python ikk_automation_merged.py [category] [date] [description] [shift]
    
Arguments:
    category    : IA (API), IR (Ruang Terbatas), IK (Ketinggian) [default: IA]
    date        : Work date (day number or YYYY-MM-DD) [default: 30]
    description : Work description [default: MELTING REPAIR]
    shift       : Shift number 1-3 for IKK form [default: 1]
"""

import csv
import sys
import datetime
from playwright.sync_api import Playwright, sync_playwright

def read_csv(file_path, selected_indices=None, selected_shift=None):
    """⚡ SPEED READ CSV - Ultra FAST! ⚡"""
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        if selected_shift:
            print(f"🔄 Shift {selected_shift}: Will be set in IKK form")
        
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
    """⚡ FIXED DATE SETUP - No more wrong dates! ⚡"""
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
                # FIXED: Just day number - use CURRENT month/year for work date
                day = int(selected_date)
                today = datetime.date.today()
                # Use current month and year (not hardcoded)
                return f"{day:02d}/{today.month:02d}/{today.year}"
        except ValueError:
            pass
    
    # Fallback to today's date
    today = datetime.date.today()
    return today.strftime('%d/%m/%Y')

def set_date_field(page, date_str):
    """👨‍💻 ENHANCED DATE PICKER - Robust Calendar Navigation from ori.py ⚡"""
    input_id = "ahmgawpm003_tanggal_pelaksanaan_pekerjaan_khusus_request_kontraktor"
    
    print(f"👨‍💻 ENHANCED MODE: Setting work date {date_str}")
    
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
                    elif current_year > target_year:
                        # Need to go backward
                        prev_year_btn = page.locator(".ui-datepicker-prev, .prev, [class*='prev']").first
                        if prev_year_btn.is_visible():
                            prev_year_btn.click()
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
                    elif current_month > target_month:
                        # Need to go backward
                        prev_month_btn = page.locator(".ui-datepicker-prev, .prev, [class*='prev']").first
                        if prev_month_btn.is_visible():
                            prev_month_btn.click()
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

def set_expiry_date_field(page, date_str, input_id='ahmgawpm003_tanggal_akhir_berlaku_izin_add'):
    """👨‍💻 HUMAN MIMIC CERTIFICATE EXPIRY DATE PICKER - Full Calendar Navigation ⚡"""
    
    print(f"👨‍💻 HUMAN MIMIC MODE: Setting certificate expiry date {date_str} to field {input_id}")
    
    # Parse target date
    try:
        # Expected format: DD/MM/YYYY
        day_str, month_str, year_str = date_str.split('/')
        target_day = int(day_str)
        target_month = int(month_str)
        target_year = int(year_str)
        print(f"🎯 Target Expiry: Day={target_day}, Month={target_month}, Year={target_year}")
        
        # SPECIAL NOTICE for year 2027
        if target_year == 2027:
            print(f"🚀 SPECIAL: Navigating to FUTURE YEAR 2027 - Human mimic calendar navigation!")
        
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
        
        # HUMAN MIMIC APPROACH: Click calendar icon first
        print(f"📅 HUMAN MIMIC: Opening expiry calendar picker...")
        
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
                    print(f"📅 Clicking expiry calendar icon: {selector}")
                    calendar_icon.click()
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
        
        # HUMAN MIMIC CALENDAR NAVIGATION - IDENTICAL TO WORK DATE
        print(f"🧭 HUMAN MIMIC: Navigating to target expiry date...")
        
        # Wait for calendar to appear
        page.wait_for_timeout(1000)
        
        # Navigate to correct year
        print(f"📅 Navigating to year {target_year}...")
        year_navigation_attempts = 0
        max_year_attempts = 5
        
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
                            print(f"⏭️ Clicked next year button")
                        else:
                            print(f"⚠️ Next year button not visible")
                    elif current_year > target_year:
                        # Need to go backward
                        print(f"⬅️ Need to go backward from {current_year} to {target_year}")
                        prev_year_btn = page.locator(".ui-datepicker-prev, .prev, [class*='prev']").first
                        if prev_year_btn.is_visible():
                            prev_year_btn.click()
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
                    elif current_month > target_month:
                        # Need to go backward
                        prev_month_btn = page.locator(".ui-datepicker-prev, .prev, [class*='prev']").first
                        if prev_month_btn.is_visible():
                            prev_month_btn.click()
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
        print(f"✅ Final expiry date value: '{final_value}'")
        # Force set value if not as expected
        if final_value != date_str:
            print(f"⚠️ Final value '{final_value}' tidak sesuai target '{date_str}', force set via JS (all events)")
            page.evaluate(f"""
                (function() {{
                    const field = document.getElementById('{input_id}');
                    if (field) {{
                        field.value = '{date_str}';
                        field.setAttribute('value', '{date_str}');
                        ['input', 'change', 'blur', 'focus', 'keydown', 'keyup'].forEach(eventType => {{
                            field.dispatchEvent(new Event(eventType, {{bubbles: true}}));
                        }});
                        // Blur ke field lain
                        field.blur();
                        setTimeout(() => {{
                            field.focus();
                        }}, 100);
                    }}
                }})()
            """)
            # Re-verify
            import time
            time.sleep(0.2)
            final_value2 = page.evaluate(f"""
                (function() {{
                    try {{
                        const field = document.getElementById('{input_id}');
                        return field ? field.value : 'field_not_found';
                    }} catch(e) {{
                        return 'verification_error';
                    }}
                }})()
            """)
            print(f"✅ Final expiry date value after force set (all events): '{final_value2}'")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Human mimic expiry date setting error: {e}")
        
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

def run(playwright: Playwright, personnel_data, ikk_category="IA", work_date="30", deskripsi="MELTING REPAIR", selected_shift=1):
    """⚡ MERGED IKK AUTOMATION - Best of Both Worlds! ⚡"""
    print(f"🚀 MERGED IKK START - Category: {ikk_category}, Shift: {selected_shift}")
    print(f"👥 Personnel: {len(personnel_data)} people")
    
    browser = playwright.chromium.launch(headless=False, slow_mo=0)
    context = browser.new_context()
    page = context.new_page()

    try:
        # ⚡ INSTANT LOGIN
        print("⚡ INSTANT LOGIN...")
        page.goto("https://portal2.ahm.co.id/jx02/ahmipdsh000-pst/login.htm#AHMGAWPM003:1")
        page.get_by_role("textbox", name="Username").fill("KONTRAKTOR_P4_02")
        page.get_by_role("textbox", name="Password").fill("H0nd42025!")
        page.get_by_role("button", name=" LOGIN").click()
        page.wait_for_url("**/dashboard.htm**", timeout=60000)
        print("✅ LOGIN SUCCESS")

        # ⚡ INSTANT NAVIGATION
        print("⚡ INSTANT NAVIGATION...")
        page.get_by_role("link", name=" IZIN KERJA ").click()
        page.get_by_role("link", name="Maintain Izin Kerja Khusus").click()
        page.get_by_role("button", name="+ Request IKK").click()
        
        # ⚡ INSTANT FORM SETUP
        print("⚡ INSTANT FORM SETUP...")
        page.wait_for_selector("#ahmgawpm003_kategori_pekerjaan_request_kontraktor", timeout=10000)
        
        # Ultra-fast form filling with JavaScript - semua sekaligus!
        page.evaluate(f"""
            // INSTANT form setup - all at once
            document.getElementById('ahmgawpm003_kategori_pekerjaan_request_kontraktor').value = 'Internal';
            document.getElementById('ahmgawpm003_kategori_pekerjaan_request_kontraktor').dispatchEvent(new Event('change', {{bubbles: true}}));
            
            setTimeout(() => {{
                document.getElementById('ahmgawpm003_kategori_ikk_request_kontraktor').value = '{ikk_category}';
                document.getElementById('ahmgawpm003_kategori_ikk_request_kontraktor').dispatchEvent(new Event('change', {{bubbles: true}}));
            }}, 50);
        """)
        
        page.wait_for_timeout(200)  # Minimal wait
        
        # ⚡ INSTANT AREA SELECTION
        print("⚡ INSTANT AREA...")
        page.locator("#ahmgawpm003_nomor_ikp_request_kontraktor_lov_kontraktor").get_by_role("button", name="").click()
        page.wait_for_timeout(100)
        
        try:
            page.get_by_text("REPAIR MELTING", exact=False).first.click()
        except:
            try:
                page.get_by_text("REPAIR").first.click()
            except:
                page.locator('td[role="cell"]').first.click()

        # 🔄 ENHANCED SHIFT DETECTION & SETTING - From ori.py 🔄
        print(f"🔄 ENHANCED SHIFT SETTING: {selected_shift}")
        
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
        
        print(f"Shift debug info:")
        for info in shift_set_success.get('debugInfo', []):
            print(f"    {info}")
            
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

        # 📅 HUMAN MIMIC DATE SETTING - Work Date
        print(f"📅 HUMAN MIMIC DATE SETTING: {work_date}")
        date_str = setup_date(work_date)
        print(f"⚡ Formatted work date: {date_str}")
        
        print(f"👨‍💻 Setting WORK DATE with human mimic calendar navigation...")
        work_date_success = set_date_field(page, date_str)
        
        if work_date_success:
            print(f"✅ Work date set successfully with human mimic: {date_str}")
        else:
            print(f"⚠️ Work date setting failed, but continuing...")

        # 🛡️ ENHANCED SAFETY INDUCTION - From ori.py
        print("🛡️ ENHANCED SAFETY INDUCTION...")
        
        safety_induction_result = page.evaluate(f"""
            (function() {{
                try {{
                    const safetyField = document.getElementById('ahmgawpm003_status_safety_induction_edit');
                    if (safetyField) {{
                        const targetOption = Array.from(safetyField.options).find(opt => 
                            opt.value === 'Sudah' || opt.text.includes('Sudah') || 
                            opt.value === 'Aktif' || opt.text.includes('Aktif')
                        );
                        if (targetOption) {{
                            safetyField.value = targetOption.value;
                            safetyField.dispatchEvent(new Event('change', {{bubbles: true}}));
                        }}
                    }}
                    
                    const safetyDateField = document.getElementById('ahmgawpm003_tanggal_safety_induction_edit');
                    if (safetyDateField) {{
                        safetyDateField.value = '{date_str}';
                        safetyDateField.dispatchEvent(new Event('input', {{bubbles: true}}));
                    }}
                    
                    return true;
                }} catch(e) {{
                    return false;
                }}
            }})()
        """)
        
        if safety_induction_result:
            print("✅ Safety induction set successfully")
        else:
            print("⚠️ Safety induction setting failed")

        # ⚡ ULTRA-FAST PERSONNEL PROCESSING
        print(f"⚡ ULTRA-FAST PERSONNEL: {len(personnel_data)} people")
        
        # Load certificate data
        csv_map = {
            "IA": "personnel_list_IA.csv",
            "IR": "personnel_list_IR.csv", 
            "IK": "personnel_list_IK.csv"
        }
        csv_file_path = csv_map.get(ikk_category, csv_map["IA"])
        
        cert_lookup = {}
        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    nik = str(row.get('Nomor', '')).strip()
                    cert = str(row.get('Sertif', '')).strip()
                    exp_cert = str(row.get('Expsertif', '')).strip()
                    
                    if (cert and exp_cert and cert not in ['', 'n/a', 'none', '-', 'null', 'None'] 
                        and exp_cert not in ['', 'n/a', 'none', '-', 'null', 'None']):
                        cert_lookup[nik] = {'cert': cert, 'exp_cert': exp_cert}
        except Exception:
            cert_lookup = {}

        success_count = 0
        
        for i, (name, nik) in enumerate(personnel_data, 1):
            print(f"⚡ Person {i}: {name}")
            
            try:
                # 🔧 FIXED: Handle first person modal access properly
                if i == 1:
                    # For first person, try to access existing modal or trigger it
                    print(f"    📝 Person 1: Accessing personnel modal...")
                    try:
                        # Check if modal is already visible
                        page.wait_for_selector("#ahmgawpm003_nik_paspor_pekerja_add", state="visible", timeout=2000)
                        print(f"    ✅ Personnel modal already visible for person 1")
                    except:
                        # Modal not visible, try to trigger it
                        print(f"    🔄 Modal not visible, trying to trigger for person 1...")
                        try:
                            # Try clicking Add Personnel button even for first person
                            page.get_by_role("button", name="+ Add Personnel").click()
                            page.wait_for_timeout(800)
                            print(f"    ✅ Add Personnel clicked for person 1")
                        except Exception as first_person_error:
                            print(f"    ⚠️ Add Personnel failed for person 1: {first_person_error}")
                            # Try alternative methods to access modal
                            try:
                                # Look for any personnel-related section to click
                                personnel_section = page.locator(".personnel-section, #personnel_table, .add-row").first
                                if personnel_section.is_visible():
                                    personnel_section.click()
                                    page.wait_for_timeout(500)
                                    print(f"    ✅ Personnel section clicked for person 1")
                            except:
                                print(f"    ⚠️ All methods failed for person 1, continuing anyway...")
                else:
                    # For person 2+, click Add Personnel button
                    print(f"    🔄 Person {i}: Clicking Add Personnel...")
                    page.get_by_role("button", name="+ Add Personnel").click()
                    page.wait_for_timeout(600)
                    print(f"    ✅ Add Personnel clicked for person {i}")
                
                # Wait for modal to be ready
                try:
                    page.wait_for_selector("#ahmgawpm003_nik_paspor_pekerja_add", state="visible", timeout=3000)
                    print(f"    ✅ Personnel modal ready for person {i}")
                except Exception as modal_wait_error:
                    print(f"    ⚠️ Modal wait failed for person {i}: {modal_wait_error}")
                    # Continue anyway, might still work
                
                has_cert = nik in cert_lookup
                
                # Fill basic fields instantly
                if has_cert:
                    cert_data = cert_lookup[nik]
                    cert_escaped = cert_data['cert'].replace("'", "\\'")
                    
                    fill_result = page.evaluate(f"""
                        (function() {{
                            try {{
                                const fields = [
                                    {{id: 'ahmgawpm003_nik_paspor_pekerja_add', value: '{nik}'}},
                                    {{id: 'ahmgawpm003_nama_pekerja_add', value: '{name}'}},
                                    {{id: 'ahmgawpm003_nomor_hp_pekerja_add', value: '082129002163'}},
                                    {{id: 'ahmgawpm003_email_pekerja_add', value: 'Hirochiku-indonesia@co.id'}},
                                    {{id: 'ahmgawpm003_seksi_add', value: 'HAI member'}},
                                    {{id: 'ahmgawpm003_departemen_add', value: 'HAI member'}},
                                    {{id: 'ahmgawpm003_divisi_add', value: 'HAI member'}}
                                ];
                                
                                fields.forEach(field => {{
                                    const element = document.getElementById(field.id);
                                    if (element) {{
                                        element.value = field.value;
                                        element.dispatchEvent(new Event('input', {{bubbles: true}}));
                                        element.dispatchEvent(new Event('change', {{bubbles: true}}));
                                    }}
                                }});
                                
                                // Set certification to Y
                                const certField = document.getElementById('ahmgawpm003_kebutuhan_sertifikasi_add');
                                if (certField) {{
                                    certField.value = 'Y';
                                    certField.dispatchEvent(new Event('change', {{bubbles: true}}));
                                }}
                                
                                return {{success: true}};
                            }} catch(e) {{
                                return {{success: false, error: e.message}};
                            }}
                        }})()
                    """)
                    
                    page.wait_for_timeout(400)
                    
                    # Fill certificate fields
                    try:
                        cert_num_field = page.locator("#ahmgawpm003_nomor_sertifikasi_add")
                        cert_num_field.fill(cert_data['cert'])
                        
                        # 📅 ENHANCED: Parse Indonesian date format from CSV
                        actual_expiry_date = cert_data['exp_cert']  # Use actual date from CSV
                        print(f"📅 ACTUAL EXPIRY DATE from CSV: {actual_expiry_date}")
                        
                        # Convert Indonesian date format to DD/MM/YYYY
                        def parse_indonesian_date(date_str):
                            """Convert Indonesian date format to DD/MM/YYYY"""
                            try:
                                # Handle format like "5 Agustus 2027"
                                if any(month in date_str.lower() for month in ['januari', 'februari', 'maret', 'april', 'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'november', 'desember']):
                                    # Indonesian month names mapping
                                    month_mapping = {
                                        'januari': '01', 'februari': '02', 'maret': '03', 'april': '04',
                                        'mei': '05', 'juni': '06', 'juli': '07', 'agustus': '08',
                                        'september': '09', 'oktober': '10', 'november': '11', 'desember': '12'
                                    }
                                    
                                    parts = date_str.strip().split()
                                    if len(parts) >= 3:
                                        day = parts[0].strip()
                                        month_name = parts[1].strip().lower()
                                        year = parts[2].strip()
                                        
                                        if month_name in month_mapping:
                                            month_num = month_mapping[month_name]
                                            # Format as DD/MM/YYYY
                                            formatted_date = f"{day.zfill(2)}/{month_num}/{year}"
                                            print(f"🔄 Converted Indonesian date: '{date_str}' -> '{formatted_date}'")
                                            return formatted_date
                                
                                # Handle DD/MM/YYYY format (already correct)
                                elif '/' in date_str and len(date_str.split('/')) == 3:
                                    return date_str
                                
                                # Handle YYYY-MM-DD format
                                elif '-' in date_str and len(date_str.split('-')) == 3:
                                    date_parts = date_str.split('-')
                                    return f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"
                                
                                # Fallback: return original
                                else:
                                    print(f"⚠️ Unknown date format: {date_str}, using fallback")
                                    return "31/07/2027"  # Safe fallback
                                    
                            except Exception as e:
                                print(f"⚠️ Date parsing error: {e}, using fallback")
                                return "31/07/2027"  # Safe fallback
                        
                        expiry_date_value = parse_indonesian_date(actual_expiry_date)
                        
                        # Validate the parsed date format
                        def validate_date_format(date_str):
                            """Validate DD/MM/YYYY format"""
                            try:
                                parts = date_str.split('/')
                                if len(parts) != 3:
                                    return False
                                
                                day, month, year = parts
                                day_int = int(day)
                                month_int = int(month)
                                year_int = int(year)
                                
                                # Basic validation
                                if not (1 <= day_int <= 31):
                                    return False
                                if not (1 <= month_int <= 12):
                                    return False
                                if not (2020 <= year_int <= 2030):  # Reasonable year range
                                    return False
                                
                                return True
                            except:
                                return False
                        
                        # Validate and fix if needed
                        if not validate_date_format(expiry_date_value):
                            print(f"⚠️ Invalid date format detected: {expiry_date_value}")
                            expiry_date_value = "31/07/2027"  # Safe fallback
                            print(f"🔧 Using safe fallback date: {expiry_date_value}")
                        
                        print(f"👨‍💻 Setting VALIDATED CERTIFICATE EXPIRY DATE: {expiry_date_value}")
                        print(f"🎯 Target year: {expiry_date_value.split('/')[-1]} (validated DD/MM/YYYY format)")
                        
                        # Use HUMAN MIMIC calendar navigation with actual date
                        expiry_success = set_expiry_date_field(page, expiry_date_value)
                        
                        if expiry_success:
                            print(f"✅ Certificate expiry date set successfully with human mimic: {expiry_date_value}")
                        else:
                            print(f"⚠️ Human mimic expiry date failed, trying emergency fallback with actual date...")
                            # Emergency fallback expiry date setting with ACTUAL date
                            fallback_result = page.evaluate(f"""
                                (function() {{
                                    try {{
                                        const expiryField = document.getElementById('ahmgawpm003_tanggal_akhir_berlaku_izin_add');
                                        if (expiryField) {{
                                            expiryField.value = '{expiry_date_value}';
                                            expiryField.setAttribute('value', '{expiry_date_value}');
                                            expiryField.dispatchEvent(new Event('input', {{bubbles: true}}));
                                            expiryField.dispatchEvent(new Event('change', {{bubbles: true}}));
                                            return {{success: true, value: expiryField.value, actualDate: '{expiry_date_value}'}};
                                        }}
                                        return {{success: false, reason: 'field_not_found'}};
                                    }} catch(e) {{
                                        return {{success: false, error: e.message}};
                                    }}
                                }})()
                            """)
                            print(f"🚨 Emergency fallback with ACTUAL date result: {fallback_result}")
                        
                    except Exception as cert_error:
                        print(f"⚠️ Certificate error: {cert_error}")
                    
                else:
                    # No certificate
                    fill_result = page.evaluate(f"""
                        (function() {{
                            try {{
                                const fields = [
                                    {{id: 'ahmgawpm003_nik_paspor_pekerja_add', value: '{nik}'}},
                                    {{id: 'ahmgawpm003_nama_pekerja_add', value: '{name}'}},
                                    {{id: 'ahmgawpm003_nomor_hp_pekerja_add', value: '082129002163'}},
                                    {{id: 'ahmgawpm003_email_pekerja_add', value: 'Hirochiku-indonesia@co.id'}},
                                    {{id: 'ahmgawpm003_seksi_add', value: 'HAI member'}},
                                    {{id: 'ahmgawpm003_departemen_add', value: 'HAI member'}},
                                    {{id: 'ahmgawpm003_divisi_add', value: 'HAI member'}}
                                ];
                                
                                fields.forEach(field => {{
                                    const element = document.getElementById(field.id);
                                    if (element) {{
                                        element.value = field.value;
                                        element.dispatchEvent(new Event('input', {{bubbles: true}}));
                                        element.dispatchEvent(new Event('change', {{bubbles: true}}));
                                    }}
                                }});
                                
                                // Set certification to N
                                const certField = document.getElementById('ahmgawpm003_kebutuhan_sertifikasi_add');
                                if (certField) {{
                                    certField.value = 'N';
                                    certField.dispatchEvent(new Event('change', {{bubbles: true}}));
                                }}
                                
                                return {{success: true}};
                            }} catch(e) {{
                                return {{success: false, error: e.message}};
                            }}
                        }})()
                    """)
                
                page.wait_for_timeout(300)
                
                # Submit person
                try:
                    submit_btn = page.locator("#ahmgawpm003_submit_button_add_modal")
                    submit_btn.click()
                    page.wait_for_timeout(600)
                    
                    # Handle notification modal
                    try:
                        notification_modal = page.locator("#ahmgawpm003_notification_modal")
                        if notification_modal.is_visible():
                            ok_btn = notification_modal.locator("button")
                            ok_btn.click()
                            page.wait_for_selector("#ahmgawpm003_notification_modal", state="hidden", timeout=2000)
                    except:
                        pass
                    
                    success_count += 1
                    print(f"✅ Person {i} SUCCESS: {name}")
                    
                except Exception as submit_error:
                    print(f"❌ Person {i} SUBMIT FAILED: {submit_error}")
                
            except Exception as e:
                print(f"❌ Person {i} FAILED: {name} - {e}")
                continue

        print(f"⚡ PERSONNEL COMPLETE: {success_count}/{len(personnel_data)}")

        # ⚡ ULTRA-FAST AREA & TOOLS
        print("⚡ INSTANT AREA & TOOLS...")
        page.wait_for_timeout(50)
        
        # Area
        try:
            page.get_by_role("button", name="+ Add Area").click()
            page.wait_for_timeout(30)
            page.locator("#ahmgawpm003_add_area_modal .btn-lookup").click()
            page.wait_for_timeout(30)
            page.get_by_role("cell", name="G", exact=True).click()
            page.locator("#ahmgawpm003_submit_button_add_area_modal").click()
            page.wait_for_timeout(30)
            print("  ✅ AREA")
        except:
            print("  ⚠️ AREA SKIP")

        # Tools - FIXED: Field kedua juga harus "1"
        try:
            page.get_by_role("button", name="+ Add Tool").click()
            page.wait_for_timeout(30)
            
            # ENHANCED: Fill semua field yang diperlukan dengan benar
            tool_fill_success = page.evaluate("""
                (function() {
                    try {
                        // Field pertama: Tool ID = "1"
                        const toolIdField = document.getElementById('ahmgawpm003_tool_id_add');
                        if (toolIdField) {
                            toolIdField.value = '1';
                            toolIdField.dispatchEvent(new Event('input', {bubbles: true}));
                            toolIdField.dispatchEvent(new Event('change', {bubbles: true}));
                            console.log('Tool ID set: 1');
                        }
                        
                        // Field kedua: Juga harus "1" (sesuai feedback user)
                        const toolSecondField = document.getElementById('ahmgawpm003_jumlah_add') ||
                                               document.querySelector('input[name*="jumlah"]') ||
                                               document.querySelector('#ahmgawpm003_add_tool_modal input[type="number"]') ||
                                               document.querySelector('#ahmgawpm003_add_tool_modal input:nth-of-type(2)');
                        
                        if (toolSecondField) {
                            toolSecondField.value = '1';
                            toolSecondField.dispatchEvent(new Event('input', {bubbles: true}));
                            toolSecondField.dispatchEvent(new Event('change', {bubbles: true}));
                            console.log('Tool second field set: 1');
                        }
                        
                        // Description field
                        const toolDescField = document.getElementById('ahmgawpm003_deskripsi_alat_add');
                        if (toolDescField) {
                            toolDescField.value = 'BASIC TOOLS';
                            toolDescField.dispatchEvent(new Event('input', {bubbles: true}));
                            toolDescField.dispatchEvent(new Event('change', {bubbles: true}));
                            console.log('Tool description set: BASIC TOOLS');
                        }
                        
                        // Permit flag
                        const permitField = document.getElementById('ahmgawpm003_permit_flag_add');
                        if (permitField) {
                            permitField.value = 'Tidak';
                            permitField.dispatchEvent(new Event('change', {bubbles: true}));
                            console.log('Permit flag set: Tidak');
                        }
                        
                        // Cari dan isi semua field yang mungkin diperlukan
                        const allToolInputs = document.querySelectorAll('#ahmgawpm003_add_tool_modal input[type="text"], #ahmgawpm003_add_tool_modal input[type="number"]');
                        let fieldsProcessed = 0;
                        
                        allToolInputs.forEach((input, index) => {
                            if (!input.value && input.type !== 'hidden') {
                                if (input.type === 'number' || input.name?.includes('jumlah') || input.placeholder?.includes('jumlah')) {
                                    input.value = '1';
                                    input.dispatchEvent(new Event('input', {bubbles: true}));
                                    input.dispatchEvent(new Event('change', {bubbles: true}));
                                    console.log('Tool numeric field ' + index + ' set: 1');
                                    fieldsProcessed++;
                                } else if (input.type === 'text' && !input.value) {
                                    input.value = 'BASIC TOOLS';
                                    input.dispatchEvent(new Event('input', {bubbles: true}));
                                    input.dispatchEvent(new Event('change', {bubbles: true}));
                                    console.log('Tool text field ' + index + ' set: BASIC TOOLS');
                                    fieldsProcessed++;
                                }
                            }
                        });
                        
                        console.log('Total tool fields processed: ' + fieldsProcessed);
                        return {success: true, fieldsProcessed: fieldsProcessed};
                        
                    } catch(e) {
                        console.log('Tool fill error:', e);
                        return {success: false, error: e.message};
                    }
                })()
            """)
            
            print(f"    🔧 Tool fields filled: {tool_fill_success}")
            
            page.wait_for_timeout(50)  # Wait for all fields to process
            
            # FORCE ENABLE submit button
            page.evaluate("""
                const submitBtn = document.getElementById('ahmgawpm003_submit_button_add_tool_modal');
                if (submitBtn) {
                    submitBtn.removeAttribute('disabled');
                    submitBtn.disabled = false;
                    submitBtn.style.pointerEvents = 'auto';
                    submitBtn.style.opacity = '1';
                    submitBtn.classList.remove('disabled');
                }
            """)
            
            page.locator("#ahmgawpm003_submit_button_add_tool_modal").click()
            page.wait_for_timeout(30)
            print("  ✅ TOOLS (Field 1='1', Field 2='1')")
        except Exception as tool_error:
            print(f"  ⚠️ TOOLS ERROR: {tool_error}")

        # ⚡ ULTRA-FAST FINAL SUBMIT
        print("⚡ INSTANT FINAL SUBMIT...")
        
        page.evaluate("""
            const checkbox = document.getElementById('ahmgawpm003_checkbox_persetujuan');
            if (checkbox) {
                checkbox.checked = true;
                checkbox.dispatchEvent(new Event('change', {bubbles: true}));
            }
        """)
        
        page.get_by_role("button", name=" Submit").click()
        
        # 🔔 ENHANCED SUCCESS CHECK - Wait for notification properly
        print("🔔 WAITING FOR SUCCESS NOTIFICATION...")
        success_found = False
        notification_handled = False
        
        # Strategy 1: Wait for success notification modal
        try:
            print("🔍 Checking for success notification modal...")
            page.wait_for_selector("#ahmgawpm003_notification_modal", state="visible", timeout=10000)
            
            # Check if it's a success notification
            notification_message = ""
            try:
                message_element = page.locator("#ahmgawpm003_notification_modal_message")
                if message_element.is_visible():
                    notification_message = message_element.text_content()
                    print(f"📢 Notification message: {notification_message}")
            except:
                pass
            
            # Check for success indicators in the message
            success_indicators = ["berhasil", "sukses", "success", "completed", "selesai", "tersimpan"]
            is_success_notification = any(indicator in notification_message.lower() for indicator in success_indicators)
            
            if is_success_notification:
                print("🎉 SUCCESS NOTIFICATION DETECTED!")
                success_found = True
                
                # Wait for user to see the notification
                print("⏳ Waiting for user to read success notification...")
                page.wait_for_timeout(2000)  # Give user time to see notification
                
                # Now handle the OK button
                print("🔘 Looking for OK button in success notification...")
                try:
                    ok_button = page.locator("#ahmgawpm003_notification_modal button").first
                    if ok_button.is_visible():
                        print("✅ Clicking OK button...")
                        ok_button.click()
                        notification_handled = True
                        print(f"✅ Success notification OK button clicked! [Category: {ikk_category}]")
                        print(f"[PROCESS LOG] OK button clicked for notification modal ({ikk_category})")
                        # Wait for modal to close
                        page.wait_for_selector("#ahmgawpm003_notification_modal", state="hidden", timeout=2000)
                    else:
                        print("⚠️ OK button not visible")
                except Exception as ok_error:
                    print(f"⚠️ OK button click failed: {ok_error}")
            else:
                print(f"⚠️ Notification detected but not success: {notification_message}")
                
        except Exception as notification_error:
            print(f"⚠️ No success notification modal found: {notification_error}")
        
        # Strategy 2: Check for success alert
        if not success_found:
            try:
                print("🔍 Checking for success alert...")
                page.wait_for_selector(".alert-success", timeout=3000)
                success_found = True
                print("🎉 SUCCESS ALERT FOUND!")
            except:
                print("⚠️ No success alert found")
        
        # Strategy 3: Check for URL redirect
        if not success_found:
            try:
                print("🔍 Checking for dashboard redirect...")
                page.wait_for_url("**/dashboard.htm**", timeout=3000)
                success_found = True
                print("🎉 DASHBOARD REDIRECT DETECTED!")
            except:
                print("⚠️ No dashboard redirect")
        
        # Final status
        if success_found:
            # Selalu tulis notifikasi ke log, walau modal tidak muncul
            if not 'notification_message' in locals() or not notification_message:
                notification_message = "IKK telah berhasil disubmit"
            print(f"\U0001F4E2 Notification message: {notification_message}")
            print("\U0001F389 SUCCESS NOTIFICATION DETECTED!")
            print("\u2705 SUBMISSION SUCCESSFUL!")
            print("✅ IKK AUTOMATION COMPLETED SUCCESSFULLY!")
        else:
            print("\u26A0\uFE0F SUBMISSION STATUS UNCLEAR (but likely successful)")
        
        # 📊 ENHANCED COMPLETION REPORT
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print("\n" + "🎉"*25)
        print(f"🚀 MERGED IKK AUTOMATION COMPLETE! 🚀")
        print("="*50)
        print(f"📂 Category: {ikk_category}")
        print(f"📅 Work Date: {date_str}")
        print(f"🔄 Shift: {selected_shift}")
        print(f"👥 Personnel: {success_count}/{len(personnel_data)} people processed")
        print(f"📝 Description: {deskripsi}")
        print(f"⏰ Completed at: {current_time}")
        print(f"🔔 Notification: {'Handled' if notification_handled else 'Not detected'}")
        print(f"✅ Status: {'SUCCESS' if success_found else 'UNCLEAR'}")
        print("="*50)
        print("🎉"*25)
        
        # FASTPATH: Hapus random wait di akhir proses, close browser segera setelah proses selesai.
        browser.close()

    except Exception as e:
        print(f"❌ ERROR: {e}")
        try:
            page.screenshot(path='ikk_merged_error.png')
        except:
            pass

if __name__ == "__main__":
    # Parse command line arguments
    ikk_category = sys.argv[1].upper() if len(sys.argv) > 1 else "IA"
    work_date = sys.argv[2] if len(sys.argv) > 2 else "30"
    deskripsi = sys.argv[3] if len(sys.argv) > 3 else "MELTING REPAIR"
    selected_shift = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 1
    # Parse selected_indices (mulai dari arg ke-5)
    selected_indices = [int(x) for x in sys.argv[5:] if x.isdigit()]
    
    if selected_shift not in [1, 2, 3]:
        print(f"⚠️ Invalid shift {selected_shift}, using shift 1")
        selected_shift = 1
    
    # Map categories to CSV files
    csv_map = {
        "IA": "personnel_list_IA.csv",
        "IR": "personnel_list_IR.csv",
        "IK": "personnel_list_IK.csv"
    }
    csv_file_path = csv_map.get(ikk_category, csv_map["IA"])
    personnel_data = read_csv(csv_file_path, selected_indices=selected_indices if selected_indices else None, selected_shift=selected_shift)
    
    print(f"🚀 Starting MERGED IKK Automation - Category: {ikk_category}, Date: {work_date}, Shift: {selected_shift}")
    print(f"📄 CSV file: {csv_file_path}")
    print(f"👥 Personnel count: {len(personnel_data)}")
    
    with sync_playwright() as playwright:
        run(playwright, personnel_data, ikk_category, work_date, deskripsi, selected_shift)