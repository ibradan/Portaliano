import sys
import csv
import datetime
import re
from playwright.sync_api import Playwright, sync_playwright

def read_csv(file_path, selected_indices=None):
    """Read personnel data from CSV file with optional row selection."""
    data = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        print(f"📁 CSV Headers: {reader.fieldnames}")
        
        if selected_indices:
            for idx in selected_indices:
                if 0 <= idx < len(rows):
                    row = rows[idx]
                    name = row.get('Nama', '').strip()
                    nik = str(row.get('Nomor', '')).strip()  # Ensure NIK is string and stripped
                    
                    if name and nik:
                        data.append((name, nik))
                        print(f"✅ Added: {name} - NIK: {nik}")
                    else:
                        print(f"⚠️ Skipped row {idx}: Missing name or NIK")
        else:
            for idx, row in enumerate(rows):
                name = row.get('Nama', '').strip()
                nik = str(row.get('Nomor', '')).strip()  # Ensure NIK is string and stripped
                
                if name and nik:
                    data.append((name, nik))
                else:
                    print(f"⚠️ Skipped row {idx}: Missing name or NIK - Name: '{name}', NIK: '{nik}'")
    
    print(f"📊 Loaded {len(data)} valid personnel records")
    return data

def setup_date(selected_date=None):
    """Prepare date string for input."""
    if selected_date:
        try:
            date_obj = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
            return date_obj.strftime('%d/%m/%Y')
        except ValueError:
            print(f"Invalid date format: {selected_date}, using today")
    
    today = datetime.date.today()
    return today.strftime('%d/%m/%Y')

def verify_date_input(page, expected_date):
    """Verify that the date has been properly set in the form."""
    input_id = "ahmgawpm002_tanggal_pekerjaan_request_kontraktor"
    
    try:
        current_value = page.locator(f"#{input_id}").input_value()
        print(f"🔍 Current date value in field: '{current_value}'")
        print(f"🎯 Expected date value: '{expected_date}'")
        
        if current_value == expected_date:
            print("✅ Date verification successful!")
            return True
        else:
            print("❌ Date verification failed!")
            return False
    except Exception as e:
        print(f"❌ Date verification error: {e}")
        return False

def debug_calendar_structure(page):
    """Debug function to analyze calendar DOM structure."""
    try:
        print("🔍 === CALENDAR DEBUGGING MODE ===")
        
        # Take screenshot of calendar
        page.screenshot(path="calendar_debug.png")
        print("📸 Calendar screenshot saved: calendar_debug.png")
        
        # Get all visible elements in calendar
        calendar_elements = page.evaluate("""
            () => {
                const results = {
                    all_visible: [],
                    calendar_containers: [],
                    navigation_buttons: [],
                    date_cells: [],
                    headers: []
                };
                
                // Find all visible elements that might be calendar related
                const allElements = document.querySelectorAll('*');
                allElements.forEach((el, index) => {
                    if (el.offsetWidth > 0 && el.offsetHeight > 0) {
                        const text = el.textContent?.trim() || '';
                        const classes = el.className || '';
                        const id = el.id || '';
                        
                        // Check for calendar containers
                        if (classes.includes('calendar') || classes.includes('datepicker') || 
                            classes.includes('picker') || id.includes('calendar') || 
                            id.includes('datepicker')) {
                            results.calendar_containers.push({
                                tag: el.tagName,
                                id: id,
                                classes: classes,
                                text: text.substring(0, 100)
                            });
                        }
                        
                        // Check for navigation buttons
                        if ((text.includes('next') || text.includes('prev') || text.includes('>') || 
                             text.includes('<') || text.includes('→') || text.includes('←')) &&
                            (el.tagName === 'BUTTON' || el.tagName === 'A' || classes.includes('btn'))) {
                            results.navigation_buttons.push({
                                tag: el.tagName,
                                id: id,
                                classes: classes,
                                text: text
                            });
                        }
                        
                        // Check for date cells
                        if ((el.tagName === 'TD' || el.tagName === 'DIV') && 
                            /^\d{1,2}$/.test(text) && text.length <= 2) {
                            results.date_cells.push({
                                tag: el.tagName,
                                id: id,
                                classes: classes,
                                text: text
                            });
                        }
                        
                        // Check for headers (month/year display)
                        if ((classes.includes('header') || classes.includes('title') || 
                             classes.includes('month') || classes.includes('year')) &&
                            text.length > 2 && text.length < 50) {
                            results.headers.push({
                                tag: el.tagName,
                                id: id,
                                classes: classes,
                                text: text
                            });
                        }
                    }
                });
                
                return results;
            }
        """)
        
        print("📋 Calendar Analysis Results:")
        print(f"📦 Calendar containers found: {len(calendar_elements['calendar_containers'])}")
        for container in calendar_elements['calendar_containers']:
            print(f"   - {container['tag']} id='{container['id']}' class='{container['classes'][:50]}...'")
        
        print(f"🧭 Navigation buttons found: {len(calendar_elements['navigation_buttons'])}")
        for btn in calendar_elements['navigation_buttons']:
            print(f"   - {btn['tag']} '{btn['text']}' class='{btn['classes'][:30]}...'")
        
        print(f"📅 Date cells found: {len(calendar_elements['date_cells'])}")
        sample_dates = calendar_elements['date_cells'][:10]  # Show first 10
        for cell in sample_dates:
            print(f"   - {cell['tag']} '{cell['text']}' class='{cell['classes'][:30]}...'")
        
        print(f"🏷️ Headers found: {len(calendar_elements['headers'])}")
        for header in calendar_elements['headers']:
            print(f"   - {header['tag']} '{header['text']}' class='{header['classes'][:30]}...'")
        
        print("🔍 === END CALENDAR DEBUGGING ===")
        return calendar_elements
        
    except Exception as e:
        print(f"❌ Calendar debugging failed: {e}")
        return None

def set_date_field(page, date_str):
    """Set date field using multiple methods with detailed debugging."""
    input_id = "ahmgawpm002_tanggal_pekerjaan_request_kontraktor"
    
    print(f"🗓️ Attempting to set date: {date_str}")
    
    # Parse date components
    day, month, year = date_str.split('/')
    target_day = int(day)
    target_month = int(month)
    target_year = int(year)
    
    print(f"📅 Target: Day={target_day}, Month={target_month}, Year={target_year}")
    
    try:
        # Method 1: Enhanced calendar method with debugging
        try:
            calendar_icon = page.locator(f"#{input_id}_span")
            if calendar_icon.is_visible():
                print("📅 Clicking calendar icon...")
                calendar_icon.click()
                page.wait_for_timeout(2000)  # Give more time for calendar to load
                
                # Debug calendar structure
                calendar_debug = debug_calendar_structure(page)
                
                if calendar_debug:
                    # Try to find month/year info from debug results
                    current_month, current_year = analyze_calendar_debug_results(calendar_debug)
                    print(f"🗓️ Detected calendar: Month={current_month}, Year={current_year}")
                    
                    # Navigate to correct month/year if needed
                    if current_month != target_month or current_year != target_year:
                        print(f"🧭 Need to navigate from {current_month}/{current_year} to {target_month}/{target_year}")
                        
                        # Try Bootstrap DateTimePicker navigation
                        navigation_success = navigate_bootstrap_calendar(page, target_month, target_year, current_month, current_year)
                        
                        if not navigation_success:
                            print("⚠️ Month navigation failed, trying alternative approach...")
                            # Try direct header click approach
                            navigation_success = try_header_navigation(page, target_month, target_year)
                        
                        if navigation_success:
                            print("✅ Calendar navigation completed")
                            page.wait_for_timeout(1000)  # Wait for calendar to update
                        else:
                            print("❌ All navigation methods failed")
                            # Continue anyway, maybe the day exists in current view
                    
                    # Now try to click the target day
                    print(f"🎯 Looking for day {target_day} in calendar...")
                    date_clicked = False
                    
                    # Try multiple approaches to click the day
                    day_selectors = [
                        f"td.day:not(.disabled):has-text('{target_day}')",
                        f"td[data-day='{target_day}']:not(.disabled)",
                        f"td.day:has-text('{target_day}'):not(.old):not(.new)",
                        f".datepicker-days td:has-text('{target_day}'):not(.disabled)",
                        f"td:has-text('{target_day}'):not(.disabled)"
                    ]
                    
                    for selector in day_selectors:
                        try:
                            day_elements = page.locator(selector)
                            count = day_elements.count()
                            print(f"🔍 Found {count} elements for selector: {selector}")
                            
                            if count > 0:
                                # Click the first non-disabled element
                                for i in range(count):
                                    try:
                                        element = day_elements.nth(i)
                                        if element.is_visible():
                                            element.click()
                                            print(f"✅ Clicked day {target_day} using: {selector} (element {i})")
                                            date_clicked = True
                                            break
                                    except Exception as e:
                                        print(f"⚠️ Failed to click element {i}: {e}")
                                        continue
                            
                            if date_clicked:
                                break
                        except Exception as e:
                            print(f"⚠️ Selector {selector} failed: {e}")
                            continue
                    
                    if date_clicked:
                        page.wait_for_timeout(1500)  # Give more time for value to be set
                        # Verify the date was set
                        current_value = page.locator(f"#{input_id}").input_value()
                        print(f"📝 Calendar result: '{current_value}' vs expected '{date_str}'")
                        
                        # Check if date matches expectation (be flexible with format)
                        if current_value and len(current_value) > 0:
                            # Try to parse and compare the actual date
                            if verify_date_match(current_value, target_day, target_month, target_year):
                                print(f"✅ Date set via calendar successfully: {current_value}")
                                return True
                            else:
                                print(f"⚠️ Date mismatch - got {current_value}, expected day {target_day}, month {target_month}, year {target_year}")
                        else:
                            print(f"⚠️ Calendar didn't set any value")
                    else:
                        print(f"❌ Could not click day {target_day} in calendar")
                else:
                    print("❌ Calendar debugging failed")
                    
        except Exception as e:
            print(f"⚠️ Calendar method failed: {e}")
    
        # Method 2: Direct JavaScript manipulation (unchanged)
        print("🔧 Trying direct JavaScript method...")
        page.evaluate(f"""
            const input = document.getElementById('{input_id}');
            if (input) {{
                // Remove readonly and set value
                input.removeAttribute('readonly');
                input.value = '{date_str}';
                input.setAttribute('value', '{date_str}');
                
                // Trigger all relevant events
                const events = ['input', 'change', 'blur', 'keyup', 'keydown', 'focus'];
                events.forEach(eventType => {{
                    const event = new Event(eventType, {{ bubbles: true, cancelable: true }});
                    input.dispatchEvent(event);
                }});
                
                // Try triggering custom AHM functions if they exist
                if (typeof ahmgawpm002_dateChange === 'function') {{
                    ahmgawpm002_dateChange();
                }}
                if (typeof ahmgawpm002_checkDateInput === 'function') {{
                    ahmgawpm002_checkDateInput(input);
                }}
            }}
        """)
        
        page.wait_for_timeout(500)
        
        # Verify JavaScript method worked
        current_value = page.locator(f"#{input_id}").input_value()
        if current_value == date_str:
            print(f"✅ Date successfully set via JavaScript: {current_value}")
            return True
    
        # Method 3: Playwright fill method (unchanged)
        print("🎭 Trying Playwright fill method...")
        date_input = page.locator(f"#{input_id}")
        date_input.clear()
        date_input.fill(date_str)
        
        # Trigger change event
        date_input.dispatch_event('change')
        page.wait_for_timeout(500)
        
        # Final verification
        final_value = date_input.input_value()
        if final_value == date_str:
            print(f"✅ Date successfully set via Playwright: {final_value}")
            return True
        
        # Method 4: Emergency method - try alternative calendar approach
        print("🚨 Trying emergency calendar method...")
        try:
            # Try clicking calendar icon again and use a different approach
            calendar_icon = page.locator(f"#{input_id}_span")
            if calendar_icon.is_visible():
                calendar_icon.click()
                page.wait_for_timeout(2000)
                
                # Try to directly set the calendar's internal date
                emergency_result = page.evaluate(f"""
                    (function() {{
                        try {{
                            // Try to find and manipulate the calendar widget
                            const calendars = document.querySelectorAll('.datepicker, .bootstrap-datetimepicker-widget, .calendar');
                            for (let calendar of calendars) {{
                                if (calendar.style.display !== 'none') {{
                                    // Try to click on month navigation first
                                    const nextBtns = calendar.querySelectorAll('.next, [data-action="next"], th.next');
                                    const targetMonth = {target_month};
                                    const currentMonth = new Date().getMonth() + 1;
                                    const monthDiff = targetMonth - currentMonth;
                                    
                                    if (monthDiff > 0) {{
                                        for (let i = 0; i < monthDiff; i++) {{
                                            for (let btn of nextBtns) {{
                                                if (btn.offsetParent !== null) {{
                                                    btn.click();
                                                    break;
                                                }}
                                            }}
                                        }}
                                    }}
                                    
                                    // Now try to click the day
                                    setTimeout(() => {{
                                        const dayElements = calendar.querySelectorAll('td');
                                        for (let day of dayElements) {{
                                            if (day.textContent.trim() === '{target_day}' && 
                                                !day.classList.contains('disabled') && 
                                                !day.classList.contains('old') && 
                                                !day.classList.contains('new')) {{
                                                day.click();
                                                return true;
                                            }}
                                        }}
                                    }}, 1000);
                                    
                                    return true;
                                }}
                            }}
                            return false;
                        }} catch (e) {{
                            console.error('Emergency method error:', e);
                            return false;
                        }}
                    }})()
                """)
                
                if emergency_result:
                    page.wait_for_timeout(2000)
                    emergency_value = date_input.input_value()
                    if emergency_value == date_str:
                        print(f"🚨✅ Emergency method succeeded: {emergency_value}")
                        return True
                    else:
                        print(f"🚨⚠️ Emergency method partial success: {emergency_value}")
        except Exception as e:
            print(f"🚨❌ Emergency method failed: {e}")
        
        print(f"❌ Date setting failed. Expected: {date_str}, Got: {final_value}")
        return False
            
    except Exception as e:
        print(f"❌ All date setting methods failed: {e}")
        return False

def analyze_calendar_debug_results(calendar_debug):
    """Analyze calendar debug results to extract month/year info."""
    try:
        print("🔍 Analyzing calendar debug results...")
        
        # Look for month/year in headers
        for header in calendar_debug['headers']:
            text = header['text'].strip()
            print(f"📝 Header text: '{text}'")
            
            text_lower = text.lower()
            # Try to extract month/year from header text
            if any(month in text_lower for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                                              'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
                                              'januari', 'februari', 'maret', 'april', 'mei', 'juni',
                                              'juli', 'agustus', 'september', 'oktober', 'november', 'desember']):
                # Try to parse this header
                month, year = parse_month_year_from_header(text)
                print(f"✅ Parsed from header: Month={month}, Year={year}")
                return month, year
        
        print("⚠️ No month/year found in headers, checking for numeric patterns...")
        
        # Try looking for date patterns in any header text
        for header in calendar_debug['headers']:
            text = header['text'].strip()
            if re.search(r'\d{1,2}[\/\-\.]\d{4}', text) or re.search(r'\d{4}[\/\-\.]\d{1,2}', text):
                month, year = parse_month_year_from_header(text)
                print(f"✅ Parsed from numeric pattern: Month={month}, Year={year}")
                return month, year
        
        # Fallback to current date
        now = datetime.datetime.now()
        print(f"⚠️ Using fallback: Month={now.month}, Year={now.year}")
        return now.month, now.year
        
    except Exception as e:
        print(f"❌ Failed to analyze calendar results: {e}")
        now = datetime.datetime.now()
        return now.month, now.year

def add_personnel(page, name, nik, common_data):
    """Add a single personnel entry with improved NIK handling (optimized for speed)."""
    page.get_by_role("button", name="+ Add New Personnel").click()

    # More robust NIK input handling
    try:
        nik_selectors = [
            "input[name='NIK / Passport*']",
            "#ahmgawpm002_nik_add",
            "input[placeholder*='NIK']",
            "input[placeholder*='Passport']",
            ".modal input[type='text']:first-of-type"
        ]
        nik_filled = False
        for selector in nik_selectors:
            try:
                nik_field = page.locator(selector).first
                if nik_field.is_visible():
                    nik_field.fill(str(nik))
                    filled_value = nik_field.input_value()
                    if filled_value == str(nik):
                        nik_filled = True
                        break
            except:
                continue
        if not nik_filled:
            nik_textbox = page.get_by_role("textbox", name="NIK / Passport*")
            nik_textbox.fill(str(nik))
    except Exception as e:
        print(f"⚠️ Warning: Issue with NIK input for {nik}: {e}")
    # Fill other fields (no waits)
    page.get_by_label("Nama Pekerja").fill(name)
    page.locator("#ahmgawpm002_alamat_add").fill(common_data['address'])
    page.locator("#ahmgawpm002_no_hp_pekerja_add").fill(common_data['phone'])
    page.get_by_role("textbox", name="Contoh format pengisian :").fill(common_data['email'])
    # Submit (no waits)
    page.locator("#ahmgawpm002_submit_add_pekerja").click()

def run(playwright: Playwright, personnel_list, selected_date=None, selected_shift=1):
    """Main automation function optimized for speed."""
    print(f"🔄 Starting IKH automation with parameters:")
    print(f"   📅 Date: {selected_date}")
    print(f"   🔄 Shift: {selected_shift}")
    print(f"   👥 Personnel count: {len(personnel_list)}")
    
    browser = playwright.chromium.launch(
        headless=False,
        args=[
            '--start-maximized',
            '--disable-web-security',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-features=VizDisplayCompositor'
        ],
        slow_mo=0  # Set to 0 for maximum speed
    )
    context = browser.new_context()
    page = context.new_page()
    common_data = {
        'address': "RT.004/RW.011, Marga Mulya, Bekasi Utara, Bekasi, West Java 17143",
        'phone': "082129002163",
        'email': "Hirochiku-indonesia@co.id"
    }
    try:
        print("🚀 Starting automation...")
        # Login sequence (no waits)
        page.goto("https://portal2.ahm.co.id/jx02/ahmipdsh000-pst/dashboard.htm")
        page.get_by_role("textbox", name="Username").fill("KONTRAKTOR_P4_02")
        page.get_by_role("textbox", name="Password").fill("H0nd42025!")
        page.get_by_role("button", name=" LOGIN").click()
        # Navigation (no waits)
        page.get_by_role("link", name=" IZIN KERJA ").click()
        page.get_by_role("link", name="Maintain Izin Kerja Harian").click()
        page.get_by_role("button", name="+ Request IKH").click()
        page.locator("#ahmgawpm002_nomor_ikp_request_kontraktor_lov_kontraktor").get_by_role("button", name="").click()
        page.get_by_role("cell", name="REPAIR MELTING HPDC HM-2700").click()

        # Set date efficiently
        date_str = setup_date(selected_date)
        input_id = "ahmgawpm002_tanggal_pekerjaan_request_kontraktor"
        date_success = set_date_field(page, date_str)
        if not date_success:
            print("⚠️ Warning: Date may not have been set correctly!")
            page.screenshot(path="date_setting_error.png")
        else:
            print("✅ Date setting confirmed successful")
        page.wait_for_timeout(500)  # Only one short wait after date set
        final_verification = verify_date_input(page, date_str)
        if not final_verification:
            print("🚨 CRITICAL: Date verification failed! Automation may fail.")
            page.screenshot(path="date_verification_failed.png")
            actual_value = page.locator(f"#{input_id}").input_value()
            print(f"🔍 FINAL DEBUG - Field contains: '{actual_value}'")

        # Set shift based on parameter with robust error handling
        print(f"🔄 Preparing to set shift to: {selected_shift}")
        
        # Pre-check: ensure shift field is available
        try:
            shift_available = page.wait_for_selector("#ahmgawpm002_shift_request_kontraktor", timeout=10000)
            if shift_available:
                print("✅ Shift field is available")
            else:
                print("⚠️ Shift field not found, but continuing...")
        except Exception as e:
            print(f"⚠️ Shift field availability check failed: {e}")
        
        shift_success = set_shift_field(page, selected_shift)
        if not shift_success:
            print("⚠️ Warning: Shift setting may not have been successful!")
            # Debug the shift field to understand what went wrong
            debug_shift_field(page)
            page.screenshot(path="shift_setting_error.png")
        else:
            print("✅ Shift setting confirmed successful")
        
        # Verify shift setting
        page.wait_for_timeout(500)
        shift_verification = verify_shift_setting(page, selected_shift)
        if not shift_verification:
            print("🚨 CRITICAL: Shift verification failed! Attempting emergency retry...")
            # Debug the shift field for verification failure
            debug_shift_field(page)
            
            # Emergency retry with different approach
            print("🚨 Attempting emergency shift retry...")
            emergency_shift_success = False
            
            try:
                # Try a more aggressive approach
                emergency_result = page.evaluate(f"""
                    (function() {{
                        const targetShift = '{selected_shift}';
                        const selects = document.querySelectorAll('select');
                        
                        for (let select of selects) {{
                            if (select.id.includes('shift') || 
                                select.name.includes('shift') ||
                                Array.from(select.options).some(opt => opt.text.includes('Shift'))) {{
                                
                                try {{
                                    // Force enable
                                    select.disabled = false;
                                    select.removeAttribute('disabled');
                                    
                                    // Set value multiple ways
                                    select.value = targetShift;
                                    select.selectedIndex = parseInt(targetShift) - 1;
                                    
                                    // Find matching option and select it
                                    for (let i = 0; i < select.options.length; i++) {{
                                        if (select.options[i].value === targetShift) {{
                                            select.selectedIndex = i;
                                            select.options[i].selected = true;
                                            break;
                                        }}
                                    }}
                                    
                                    // Trigger comprehensive events
                                    ['focus', 'click', 'change', 'input', 'blur'].forEach(eventType => {{
                                        select.dispatchEvent(new Event(eventType, {{ bubbles: true, cancelable: true }}));
                                    }});
                                    
                                    // Verify
                                    if (select.value === targetShift) {{
                                        return {{ success: true, id: select.id, value: select.value }};
                                    }}
                                }} catch (e) {{
                                    console.error('Emergency retry error:', e);
                                }}
                            }}
                        }}
                        
                        return {{ success: false, error: 'No suitable shift field found' }};
                    }})()
                """)
                
                print(f"🚨 Emergency retry result: {emergency_result}")
                
                if emergency_result.get('success'):
                    emergency_shift_success = True
                    print(f"✅ Emergency shift retry successful!")
                    
            except Exception as e:
                print(f"❌ Emergency shift retry failed: {e}")
            
            if not emergency_shift_success:
                print("🚨 ALL SHIFT SETTING ATTEMPTS FAILED!")
                page.screenshot(path="shift_critical_failure.png")
                print("📸 Critical failure screenshot saved")
                # Continue automation but with warning
                print("⚠️ Continuing automation with potentially incorrect shift...")
            else:
                # Re-verify after emergency fix
                final_verification = verify_shift_setting(page, selected_shift)
                if final_verification:
                    print("✅ Emergency shift fix verified!")
                else:
                    print("⚠️ Emergency shift fix could not be verified")
                    
            page.screenshot(path="shift_verification_failed.png")

        # Process personnel efficiently
        total = len(personnel_list)
        print(f"👥 Processing {total} personnel records...")

        for idx, (name, nik) in enumerate(personnel_list, 1):
            try:
                print(f"🔄 Processing {idx}/{total}: {name} (NIK: {nik})")
                add_personnel(page, name, nik, common_data)

                # Progress update every 5 entries or at milestones
                if idx % 5 == 0 or idx == total:
                    percent = int((idx/total)*100)
                    print(f"⏳ Progress: {percent}% ({idx}/{total})")
                    sys.stdout.flush()

            except Exception as e:
                print(f"❌ Failed to add {name} (NIK: {nik}): {e}")
                # Take screenshot for debugging
                try:
                    page.screenshot(path=f"error_personnel_{idx}.png")
                    print(f"📸 Screenshot saved: error_personnel_{idx}.png")
                except:
                    pass
                continue
        # Final submission steps (no waits)
        page.get_by_role("button", name="+ Add New Area").click()
        page.locator("#ahmgawpm002_add_area_modal").get_by_role("button", name="").click()
        page.get_by_role("cell", name="G", exact=True).click()
        page.locator("#ahmgawpm002_submit_area_pekerjaan").click()
        page.locator(".maincontent_containers").click()
        page.locator("#ahmgawpm002_halaman_request div").filter(has_text="Dengan ini saya menyatakan").nth(1).click()
        page.locator("#ahmgawpm002_checkbox_persetujuan").check()
        page.get_by_role("button", name=" Submit").click()
        page.get_by_role("button", name=" OK").click()
        print("✅ Automation completed successfully!")
        page.wait_for_timeout(1000)
    except Exception as e:
        print(f"❌ Automation failed: {e}")
        raise
    finally:
        context.close()
        browser.close()

def get_calendar_month_year(page):
    """Get current month and year from calendar picker."""
    try:
        # Try different selectors for calendar header
        header_selectors = [
            ".calendar-header .month-year",
            ".datepicker-header .month-year",
            ".ui-datepicker-title",
            ".calendar-title",
            ".datepicker .header",
            ".month-year-display"
        ]
        
        for selector in header_selectors:
            try:
                header_element = page.locator(selector)
                if header_element.is_visible():
                    header_text = header_element.text_content()
                    print(f"📅 Calendar header found: '{header_text}'")
                    # Parse month/year from header text
                    # This will need to be adjusted based on actual format
                    return parse_month_year_from_header(header_text)
            except:
                continue
        
        # Fallback: try to get current date
        import datetime
        now = datetime.datetime.now()
        print(f"⚠️ Calendar header not found, using current date: {now.month}/{now.year}")
        return now.month, now.year
        
    except Exception as e:
        print(f"❌ Failed to get calendar month/year: {e}")
        import datetime
        now = datetime.datetime.now()
        return now.month, now.year

def parse_month_year_from_header(header_text):
    """Parse month and year from calendar header text."""
    try:
        print(f"🔍 Parsing header: '{header_text}'")
        # Try to find year (4 digits)
        year_match = re.search(r'(\d{4})', header_text)
        if year_match:
            year = int(year_match.group(1))
            print(f"📅 Found year: {year}")
        else:
            year = datetime.datetime.now().year
            print(f"📅 Using current year: {year}")
        # Month name mapping (English and Indonesian)
        month_names = {
            'january': 1, 'januari': 1, 'jan': 1,
            'february': 2, 'februari': 2, 'feb': 2,
            'march': 3, 'maret': 3, 'mar': 3,
            'april': 4, 'apr': 4,
            'may': 5, 'mei': 5,
            'june': 6, 'juni': 6, 'jun': 6,
            'july': 7, 'juli': 7, 'jul': 7,
            'august': 8, 'agustus': 8, 'aug': 8,
            'september': 9, 'sep': 9,
            'october': 10, 'oktober': 10, 'oct': 10,
            'november': 11, 'nov': 11,
            'december': 12, 'desember': 12, 'dec': 12
        }
        # Try to find month name
        header_lower = header_text.lower()
        month = datetime.datetime.now().month  # default
        for name, num in month_names.items():
            if name in header_lower:
                month = num
                print(f"📅 Found month by name '{name}': {month}")
                break
        # Try numeric month format like "07/2025" or "2025-07"
        month_match = re.search(r'(\d{1,2})[\/\-\.](\d{4})', header_text)
        if month_match:
            month = int(month_match.group(1))
            year = int(month_match.group(2))
            print(f"📅 Found month/year pattern: {month}/{year}")
        else:
            # Try reverse pattern "2025/07" or "2025-07"
            year_month_match = re.search(r'(\d{4})[\/\-\.](\d{1,2})', header_text)
            if year_month_match:
                year = int(year_month_match.group(1))
                month = int(year_month_match.group(2))
                print(f"📅 Found year/month pattern: {month}/{year}")
        print(f"✅ Final parsed result: Month={month}, Year={year}")
        return month, year
    except Exception as e:
        print(f"❌ Failed to parse header '{header_text}': {e}")
        now = datetime.datetime.now()
        print(f"📅 Using fallback: Month={now.month}, Year={now.year}")
        return now.month, now.year

def navigate_to_month_year(page, target_month, target_year, current_month, current_year):
    """Navigate calendar to target month/year."""
    try:
        print(f"🧭 Navigating from {current_month}/{current_year} to {target_month}/{target_year}")
        
        # Calculate how many months to navigate
        current_total = current_year * 12 + current_month
        target_total = target_year * 12 + target_month
        months_diff = target_total - current_total
        
        print(f"📊 Need to navigate {months_diff} months")
        
        if months_diff == 0:
            print("✅ Already at target month/year")
            return True
        
        # Find navigation buttons
        next_selectors = [
            ".next-month", ".calendar-next", ".ui-datepicker-next", 
            ".datepicker-next", "button[title*='next']", ".next"
        ]
        prev_selectors = [
            ".prev-month", ".calendar-prev", ".ui-datepicker-prev", 
            ".datepicker-prev", "button[title*='prev']", ".prev"
        ]
        
        if months_diff > 0:
            # Navigate forward
            for _ in range(abs(months_diff)):
                clicked = False
                for selector in next_selectors:
                    try:
                        next_btn = page.locator(selector)
                        if next_btn.is_visible():
                            next_btn.click()
                            print(f"➡️ Clicked next using: {selector}")
                            clicked = True
                            page.wait_for_timeout(300)
                            break
                    except:
                        continue
                if not clicked:
                    print("❌ Could not find next button")
                    return False
        else:
            # Navigate backward
            for _ in range(abs(months_diff)):
                clicked = False
                for selector in prev_selectors:
                    try:
                        prev_btn = page.locator(selector)
                        if prev_btn.is_visible():
                            prev_btn.click()
                            print(f"⬅️ Clicked prev using: {selector}")
                            clicked = True
                            page.wait_for_timeout(300)
                            break
                    except:
                        continue
                if not clicked:
                    print("❌ Could not find prev button")
                    return False
        
        print("✅ Month navigation completed")
        return True
        
    except Exception as e:
        print(f"❌ Navigation failed: {e}")
        return False

def navigate_bootstrap_calendar(page, target_month, target_year, current_month, current_year):
    """Navigate Bootstrap DateTimePicker calendar to target month/year."""
    try:
        print(f"🧭 Bootstrap navigation: {current_month}/{current_year} → {target_month}/{target_year}")
        
        # Calculate months difference
        current_total = current_year * 12 + current_month
        target_total = target_year * 12 + target_month
        months_diff = target_total - current_total
        
        if months_diff == 0:
            print("✅ Already at target month/year")
            return True
        
        print(f"📊 Need to navigate {months_diff} months ({'forward' if months_diff > 0 else 'backward'})")
        
        # Bootstrap DateTimePicker navigation selectors (expanded list)
        navigation_selectors = {
            'next': [
                '.datepicker-days .next',
                '.bootstrap-datetimepicker-widget .next',
                'th.next',
                '.next',
                '[data-action="next"]',
                '.picker-switch + th',
                'th.next:not(.disabled)',
                '.datepicker .next',
                '.calendar-next'
            ],
            'prev': [
                '.datepicker-days .prev', 
                '.bootstrap-datetimepicker-widget .prev',
                'th.prev',
                '.prev',
                '[data-action="previous"]',
                'th + .picker-switch',
                'th.prev:not(.disabled)',
                '.datepicker .prev',
                '.calendar-prev'
            ]
        }
        
        direction = 'next' if months_diff > 0 else 'prev'
        steps = abs(months_diff)
        
        for step in range(steps):
            clicked = False
            print(f"🔄 Step {step+1}/{steps}: Looking for {direction} button...")
            
            for selector in navigation_selectors[direction]:
                try:
                    nav_btn = page.locator(selector)
                    count = nav_btn.count()
                    print(f"🔍 Checking selector '{selector}': found {count} elements")
                    
                    if count > 0:
                        for i in range(count):
                            try:
                                element = nav_btn.nth(i)
                                if element.is_visible() and element.is_enabled():
                                    element.click()
                                    print(f"{'➡️' if direction == 'next' else '⬅️'} Clicked {direction} using: {selector} (element {i}, step {step+1}/{steps})")
                                    clicked = True
                                    page.wait_for_timeout(1000)  # Wait for calendar to update
                                    break
                            except Exception as e:
                                print(f"⚠️ Failed to click element {i} with selector {selector}: {e}")
                                continue
                    
                    if clicked:
                        break
                        
                except Exception as e:
                    print(f"⚠️ Failed with selector {selector}: {e}")
                    continue
            
            if not clicked:
                print(f"❌ Could not find working {direction} button for step {step+1}")
                print("🔍 Trying to debug available navigation elements...")
                
                # Debug: show all clickable elements that might be navigation
                debug_nav = page.evaluate("""
                    () => {
                        const elements = document.querySelectorAll('th, button, .next, .prev, [data-action]');
                        return Array.from(elements).map(el => ({
                            tag: el.tagName,
                            classes: el.className,
                            text: el.textContent.trim(),
                            visible: el.offsetParent !== null,
                            id: el.id
                        })).filter(el => el.visible && (el.text.includes('>') || el.text.includes('<') || el.classes.includes('next') || el.classes.includes('prev')));
                    }
                """)
                
                print(f"🔍 Available navigation elements: {debug_nav}")
                return False
        
        print("✅ Navigation completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Bootstrap navigation failed: {e}")
        return False

def try_header_navigation(page, target_month, target_year):
    """Try alternative navigation by clicking on month/year headers."""
    try:
        print(f"🎯 Trying header navigation to {target_month}/{target_year}")
        
        # Look for clickable month/year headers
        header_selectors = [
            '.picker-switch',
            '.datepicker-switch',
            '.bootstrap-datetimepicker-widget .picker-switch',
            'th.picker-switch',
            '.month-year-header'
        ]
        
        for selector in header_selectors:
            try:
                header = page.locator(selector)
                if header.is_visible():
                    print(f"🔍 Found header: {selector}")
                    header_text = header.text_content()
                    print(f"📝 Header text: '{header_text}'")
                    
                    # Try clicking the header to get month/year picker
                    header.click()
                    page.wait_for_timeout(1000)
                    
                    # Look for month picker view
                    month_selectors = [
                        f'[data-month="{target_month-1}"]',  # 0-based months
                        f'.month:has-text("{get_month_name(target_month)}")',
                        f'td:has-text("{get_month_name(target_month)}")',
                        f'span:has-text("{get_month_name(target_month)}")'
                    ]
                    
                    month_clicked = False
                    for month_sel in month_selectors:
                        try:
                            month_elem = page.locator(month_sel)
                            if month_elem.is_visible():
                                month_elem.click()
                                print(f"📅 Clicked month using: {month_sel}")
                                month_clicked = True
                                page.wait_for_timeout(500)
                                break
                        except:
                            continue
                    
                    if month_clicked:
                        # Now try to select year if needed
                        year_selectors = [
                            f'[data-year="{target_year}"]',
                            f'.year:has-text("{target_year}")',
                            f'td:has-text("{target_year}")',
                            f'span:has-text("{target_year}")'
                        ]
                        
                        for year_sel in year_selectors:
                            try:
                                year_elem = page.locator(year_sel)
                                if year_elem.is_visible():
                                    year_elem.click()
                                    print(f"📅 Clicked year using: {year_sel}")
                                    page.wait_for_timeout(500)
                                    break
                            except:
                                continue
                        
                        return True
                        
            except Exception as e:
                print(f"⚠️ Header selector {selector} failed: {e}")
                continue
        
        return False
        
    except Exception as e:
        print(f"❌ Header navigation failed: {e}")
        return False

def get_month_name(month_num):
    """Get month name for month number (1-12)."""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months[month_num - 1] if 1 <= month_num <= 12 else str(month_num)

def verify_date_match(value_str, target_day, target_month, target_year):
    """Verify if the date string matches the target date."""
    try:
        # Handle various date formats
        import re
        from datetime import datetime
        
        # Common date patterns
        patterns = [
            r'(\d{1,2})-(\w{3})-(\d{4})',  # 03-Jul-2025
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # 03/07/2025
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # 2025-07-03
            r'(\w{3}) (\d{1,2}), (\d{4})'   # Jul 03, 2025
        ]
        
        for pattern in patterns:
            match = re.match(pattern, value_str)
            if match:
                parts = match.groups()
                
                if pattern == patterns[0]:  # 03-Jul-2025
                    day, month_str, year = parts
                    month_map = {
                        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
                    }
                    month = month_map.get(month_str, 0)
                    return int(day) == target_day and month == target_month and int(year) == target_year
                
                elif pattern == patterns[1]:  # 03/07/2025
                    day, month, year = parts
                    return int(day) == target_day and int(month) == target_month and int(year) == target_year
                
                # Add more pattern handlers as needed
        
        print(f"⚠️ Could not parse date format: {value_str}")
        return False
        
    except Exception as e:
        print(f"⚠️ Date verification error: {e}")
        return False
def debug_date_area(page, input_id):
    """Debug the entire date input area to understand the structure."""
    try:
        print("🔍 === DATE AREA DEBUGGING ===")
        
        # Get info about the date input and surrounding elements
        date_area_info = page.evaluate(f"""
            () => {{
                const input = document.getElementById('{input_id}');
                const results = {{
                    input_info: null,
                    parent_info: null,
                    siblings: [],
                    nearby_spans: [],
                    nearby_buttons: [],
                    all_date_related: []
                }};
                
                if (input) {{
                    // Input info
                    results.input_info = {{
                        id: input.id,
                        value: input.value,
                        type: input.type,
                        readonly: input.readOnly,
                        disabled: input.disabled,
                        placeholder: input.placeholder,
                        classes: input.className,
                        style: input.style.cssText
                    }};
                    
                    // Parent info
                    if (input.parentElement) {{
                        results.parent_info = {{
                            tag: input.parentElement.tagName,
                            id: input.parentElement.id,
                            classes: input.parentElement.className
                        }};
                    }}
                    
                    // Siblings
                    if (input.parentElement) {{
                        Array.from(input.parentElement.children).forEach(child => {{
                            results.siblings.push({{
                                tag: child.tagName,
                                id: child.id,
                                classes: child.className,
                                text: child.textContent?.trim()?.substring(0, 50) || ''
                            }});
                        }});
                    }}
                    
                    // Look for spans with similar ID pattern
                    const spanPattern = input.id + '_span';
                    const spanElement = document.getElementById(spanPattern);
                    if (spanElement) {{
                        results.nearby_spans.push({{
                            id: spanElement.id,
                            tag: spanElement.tagName,
                            classes: spanElement.className,
                            text: spanElement.textContent?.trim() || '',
                            clickable: spanElement.onclick !== null
                        }});
                    }}
                    
                    // Look for buttons near the input
                    const allButtons = document.querySelectorAll('button, a, span[onclick], div[onclick]');
                    allButtons.forEach(btn => {{
                        const rect = btn.getBoundingClientRect();
                        const inputRect = input.getBoundingClientRect();
                        const distance = Math.abs(rect.left - inputRect.right);
                        
                        if (distance < 100 && rect.top >= inputRect.top - 50 && rect.top <= inputRect.bottom + 50) {{
                            results.nearby_buttons.push({{
                                tag: btn.tagName,
                                id: btn.id,
                                classes: btn.className,
                                text: btn.textContent?.trim()?.substring(0, 30) || '',
                                onclick: btn.onclick !== null,
                                distance: Math.round(distance)
                            }});
                        }}
                    }});
                    
                    // Look for any element with 'date', 'calendar', 'picker' in id or class
                    const allElements = document.querySelectorAll('*');
                    allElements.forEach(el => {{
                        const id = el.id?.toLowerCase() || '';
                        const classes = el.className?.toLowerCase() || '';
                        
                        if ((id.includes('date') || id.includes('calendar') || id.includes('picker') ||
                             classes.includes('date') || classes.includes('calendar') || classes.includes('picker')) &&
                            el.offsetWidth > 0 && el.offsetHeight > 0) {{
                            results.all_date_related.push({{
                                tag: el.tagName,
                                id: el.id,
                                classes: el.className,
                                text: el.textContent?.trim()?.substring(0, 50) || ''
                            }});
                        }}
                    }});
                }}
                
                return results;
            }}
        """)
        
        print("📋 Date Area Analysis:")
        if date_area_info['input_info']:
            print(f"📝 Input: {date_area_info['input_info']}")
            print(f"👨‍👩‍👧‍👦 Parent: {date_area_info['parent_info']}")
            print(f"👥 Siblings: {len(date_area_info['siblings'])}")
            for sibling in date_area_info['siblings']:
                print(f"   - {sibling['tag']} id='{sibling['id']}' class='{sibling['classes'][:30]}...' text='{sibling['text']}'")
            
            print(f"🏷️ Nearby spans: {len(date_area_info['nearby_spans'])}")
            for span in date_area_info['nearby_spans']:
                print(f"   - {span['tag']} id='{span['id']}' clickable={span['clickable']}")
                
            print(f"🔘 Nearby buttons: {len(date_area_info['nearby_buttons'])}")
            for btn in date_area_info['nearby_buttons']:
                print(f"   - {btn['tag']} '{btn['text']}' distance={btn['distance']}px onclick={btn['onclick']}")
            
            print(f"📅 Date-related elements: {len(date_area_info['all_date_related'])}")
            for el in date_area_info['all_date_related'][:10]:  # Show first 10
                print(f"   - {el['tag']} id='{el['id']}' class='{el['classes'][:30]}...'")
        else:
            print("❌ Date input not found!")
        
        print("🔍 === END DATE AREA DEBUGGING ===")
        return date_area_info
        
    except Exception as e:
        print(f"❌ Date area debugging failed: {e}")
        return None

def set_shift_field(page, selected_shift):
    """Set shift field using multiple robust methods with comprehensive error handling."""
    shift_id = "ahmgawpm002_shift_request_kontraktor"
    
    # Validate and normalize shift value
    if selected_shift not in [1, 2, 3]:
        print(f"⚠️ Invalid shift value {selected_shift}, defaulting to 1")
        selected_shift = 1
    
    shift_value = str(selected_shift)
    print(f"🔄 Setting shift to: {shift_value}")
    
    try:
        # Method 1: Standard Playwright select_option
        try:
            print("🎯 Method 1: Standard select_option...")
            shift_locator = page.locator(f"#{shift_id}")
            
            # Wait for element to be available
            shift_locator.wait_for(state="visible", timeout=5000)
            
            # Check if element is enabled
            if not shift_locator.is_enabled():
                print("⚠️ Shift field is disabled, trying to enable...")
                page.evaluate(f"""
                    const select = document.getElementById('{shift_id}');
                    if (select) {{
                        select.disabled = false;
                        select.removeAttribute('disabled');
                    }}
                """)
                page.wait_for_timeout(500)
            
            # Select the option
            shift_locator.select_option(shift_value)
            page.wait_for_timeout(1000)
            
            # Verify selection
            selected_value = shift_locator.input_value()
            if selected_value == shift_value:
                print(f"✅ Method 1 successful: {selected_value}")
                return True
            else:
                print(f"⚠️ Method 1 failed: expected {shift_value}, got {selected_value}")
                
        except Exception as e:
            print(f"⚠️ Method 1 failed: {e}")
    
        # Method 2: JavaScript manipulation
        try:
            print("🔧 Method 2: JavaScript manipulation...")
            js_result = page.evaluate(f"""
                (function() {{
                    try {{
                        const select = document.getElementById('{shift_id}');
                        if (!select) {{
                            return {{ success: false, error: 'Element not found' }};
                        }}
                        
                        // Enable the select if disabled
                        select.disabled = false;
                        select.removeAttribute('disabled');
                        
                        // Set the value
                        select.value = '{shift_value}';
                        
                        // Trigger events to ensure the change is detected
                        const events = ['input', 'change', 'blur', 'focus'];
                        events.forEach(eventType => {{
                            const event = new Event(eventType, {{ bubbles: true, cancelable: true }});
                            select.dispatchEvent(event);
                        }});
                        
                        // Verify the value was set
                        const finalValue = select.value;
                        return {{ 
                            success: finalValue === '{shift_value}', 
                            value: finalValue,
                            options: Array.from(select.options).map(opt => ({{ value: opt.value, text: opt.text }}))
                        }};
                    }} catch (e) {{
                        return {{ success: false, error: e.message }};
                    }}
                }})()
            """)
            
            print(f"📊 JavaScript result: {js_result}")
            
            if js_result.get('success'):
                print(f"✅ Method 2 successful: {js_result.get('value')}")
                return True
            else:
                print(f"⚠️ Method 2 failed: {js_result.get('error')}")
                available_options = js_result.get('options', [])
                print(f"🔍 Available options: {available_options}")
                
        except Exception as e:
            print(f"⚠️ Method 2 failed: {e}")
    
        # Method 3: Direct option clicking
        try:
            print("🎯 Method 3: Direct option clicking...")
            
            # Find and click the specific option
            option_selectors = [
                f"#{shift_id} option[value='{shift_value}']",
                f"#{shift_id} option:nth-child({int(shift_value) + 1})",  # +1 because options might be 1-indexed
                f"select#{shift_id} option[value='{shift_value}']"
            ]
            
            option_clicked = False
            for selector in option_selectors:
                try:
                    option_element = page.locator(selector)
                    if option_element.count() > 0 and option_element.is_visible():
                        option_element.click()
                        print(f"✅ Clicked option using selector: {selector}")
                        option_clicked = True
                        page.wait_for_timeout(1000)
                        break
                except Exception as e:
                    print(f"⚠️ Option selector {selector} failed: {e}")
                    continue
            
            if option_clicked:
                # Verify the selection
                final_value = page.locator(f"#{shift_id}").input_value()
                if final_value == shift_value:
                    print(f"✅ Method 3 successful: {final_value}")
                    return True
                else:
                    print(f"⚠️ Method 3 partial success: expected {shift_value}, got {final_value}")
            else:
                print("❌ Method 3 failed: Could not click any option")
                
        except Exception as e:
            print(f"⚠️ Method 3 failed: {e}")
    
        # Method 4: Force keyboard navigation
        try:
            print("⌨️ Method 4: Keyboard navigation...")
            
            shift_locator = page.locator(f"#{shift_id}")
            
            # Focus on the select element
            shift_locator.focus()
            page.wait_for_timeout(500)
            
            # Use keyboard navigation to select the option
            # Reset to first option
            shift_locator.press("Home")
            page.wait_for_timeout(300)
            
            # Navigate to the desired option (1-based)
            for i in range(int(shift_value) - 1):
                shift_locator.press("ArrowDown")
                page.wait_for_timeout(200)
            
            # Confirm selection
            shift_locator.press("Enter")
            page.wait_for_timeout(1000)
            
            # Verify
            keyboard_value = shift_locator.input_value()
            if keyboard_value == shift_value:
                print(f"✅ Method 4 successful: {keyboard_value}")
                return True
            else:
                print(f"⚠️ Method 4 failed: expected {shift_value}, got {keyboard_value}")
                
        except Exception as e:
            print(f"⚠️ Method 4 failed: {e}")
    
        # Method 5: Emergency fallback - find all selects and try them
        try:
            print("🚨 Method 5: Emergency fallback...")
            
            all_selects_result = page.evaluate(f"""
                (function() {{
                    const allSelects = document.querySelectorAll('select');
                    const results = [];
                    
                    for (let select of allSelects) {{
                        if (select.id.includes('shift') || 
                            select.name.includes('shift') ||
                            select.className.includes('shift')) {{
                            
                            try {{
                                select.value = '{shift_value}';
                                select.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                
                                results.push({{
                                    id: select.id,
                                    name: select.name,
                                    value: select.value,
                                    success: select.value === '{shift_value}'
                                }});
                            }} catch (e) {{
                                results.push({{
                                    id: select.id,
                                    name: select.name,
                                    error: e.message
                                }});
                            }}
                        }}
                    }}
                    
                    return results;
                }})()
            """)
            
            print(f"🔍 Emergency scan results: {all_selects_result}")
            
            # Check if any of the emergency attempts succeeded
            for result in all_selects_result:
                if result.get('success'):
                    print(f"✅ Method 5 found working select: {result['id']}")
                    return True
                    
        except Exception as e:
            print(f"⚠️ Method 5 failed: {e}")
    
        # Final verification attempt
        try:
            final_check = page.locator(f"#{shift_id}").input_value()
            print(f"🔍 Final shift field value: '{final_check}'")
            
            # Even if our methods failed, check if the value is somehow correct
            if final_check == shift_value:
                print(f"✅ Shift value is correct despite method failures: {final_check}")
                return True
            
        except Exception as e:
            print(f"⚠️ Final verification failed: {e}")
    
        print(f"❌ All shift setting methods failed for value: {shift_value}")
        return False
        
    except Exception as e:
        print(f"❌ Critical error in shift setting: {e}")
        return False

def verify_shift_setting(page, expected_shift):
    """Verify that the shift has been properly set."""
    shift_id = "ahmgawpm002_shift_request_kontraktor"
    
    try:
        current_value = page.locator(f"#{shift_id}").input_value()
        expected_value = str(expected_shift)
        
        print(f"🔍 Current shift value: '{current_value}'")
        print(f"🎯 Expected shift value: '{expected_value}'")
        
        if current_value == expected_value:
            print("✅ Shift verification successful!")
            return True
        else:
            print("❌ Shift verification failed!")
            
            # Try to get more info about the select element
            shift_info = page.evaluate(f"""
                (function() {{
                    const select = document.getElementById('{shift_id}');
                    if (!select) return {{ error: 'Element not found' }};
                    
                    return {{
                        value: select.value,
                        selectedIndex: select.selectedIndex,
                        options: Array.from(select.options).map((opt, idx) => ({{
                            index: idx,
                            value: opt.value,
                            text: opt.text,
                            selected: opt.selected
                        }})),
                        disabled: select.disabled
                    }};
                }})()
            """)
            
            print(f"🔍 Detailed shift info: {shift_info}")
            return False
            
    except Exception as e:
        print(f"❌ Shift verification error: {e}")
        return False

def debug_shift_field(page):
    """Debug the shift field to understand its structure and state."""
    shift_id = "ahmgawpm002_shift_request_kontraktor"
    
    try:
        print("🔍 === SHIFT FIELD DEBUGGING ===")
        
        shift_debug_info = page.evaluate(f"""
            (function() {{
                const select = document.getElementById('{shift_id}');
                const results = {{
                    element_found: false,
                    element_info: null,
                    options: [],
                    parent_info: null,
                    nearby_elements: [],
                    computed_styles: null
                }};
                
                if (select) {{
                    results.element_found = true;
                    
                    // Basic element info
                    results.element_info = {{
                        tag: select.tagName,
                        id: select.id,
                        name: select.name,
                        value: select.value,
                        selectedIndex: select.selectedIndex,
                        disabled: select.disabled,
                        readonly: select.readOnly,
                        required: select.required,
                        className: select.className,
                        style: select.style.cssText
                    }};
                    
                    // Options info
                    Array.from(select.options).forEach((option, index) => {{
                        results.options.push({{
                            index: index,
                            value: option.value,
                            text: option.text,
                            selected: option.selected,
                            disabled: option.disabled
                        }});
                    }});
                    
                    // Parent info
                    if (select.parentElement) {{
                        results.parent_info = {{
                            tag: select.parentElement.tagName,
                            id: select.parentElement.id,
                            className: select.parentElement.className
                        }};
                    }}
                    
                    // Nearby elements (labels, siblings, etc.)
                    const parent = select.parentElement;
                    if (parent) {{
                        Array.from(parent.children).forEach(child => {{
                            if (child !== select) {{
                                results.nearby_elements.push({{
                                    tag: child.tagName,
                                    id: child.id,
                                    className: child.className,
                                    text: child.textContent?.trim()?.substring(0, 50) || ''
                                }});
                            }}
                        }});
                    }}
                    
                    // Computed styles
                    const computedStyle = window.getComputedStyle(select);
                    results.computed_styles = {{
                        display: computedStyle.display,
                        visibility: computedStyle.visibility,
                        opacity: computedStyle.opacity,
                        pointerEvents: computedStyle.pointerEvents,
                        zIndex: computedStyle.zIndex
                    }};
                }}
                
                return results;
            }})()
        """)
        
        print("📋 Shift Field Analysis:")
        if shift_debug_info['element_found']:
            print(f"✅ Element found: {shift_debug_info['element_info']}")
            print(f"📜 Available options:")
            for option in shift_debug_info['options']:
                selected_marker = " ⭐" if option['selected'] else ""
                disabled_marker = " ❌" if option['disabled'] else ""
                print(f"   [{option['index']}] value='{option['value']}' text='{option['text']}'{selected_marker}{disabled_marker}")
            
            print(f"👨‍👩‍👧‍👦 Parent: {shift_debug_info['parent_info']}")
            print(f"🎨 Computed styles: {shift_debug_info['computed_styles']}")
            
            if shift_debug_info['nearby_elements']:
                print(f"👥 Nearby elements:")
                for element in shift_debug_info['nearby_elements']:
                    print(f"   - {element['tag']} id='{element['id']}' text='{element['text']}'")
        else:
            print("❌ Shift field not found!")
            
            # Search for similar elements
            similar_elements = page.evaluate("""
                (function() {{
                    const allSelects = document.querySelectorAll('select');
                    return Array.from(allSelects).map(select => ({{
                        id: select.id,
                        name: select.name,
                        className: select.className,
                        optionsCount: select.options.length,
                        value: select.value
                    }}));
                }})()
            """)
            
            print(f"🔍 All select elements found: {similar_elements}")
        
        print("🔍 === END SHIFT FIELD DEBUGGING ===")
        return shift_debug_info
        
    except Exception as e:
        print(f"❌ Shift field debugging failed: {e}")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='IKH Automation Script - Optimized')
    parser.add_argument('csv_file_path', help='Path to CSV file')
    parser.add_argument('selected_indices', nargs='*', type=int, help='Selected row indices')
    parser.add_argument('--date', help='Selected date in YYYY-MM-DD format')
    parser.add_argument('--shift', type=int, default=1, help='Selected shift (1, 2, or 3)')
    
    args = parser.parse_args()
    
    personnel_list = read_csv(args.csv_file_path, args.selected_indices)
    
    if not personnel_list:
        print("❌ No personnel data found")
        sys.exit(1)
        
    with sync_playwright() as playwright:
        run(playwright, personnel_list, args.date, args.shift)