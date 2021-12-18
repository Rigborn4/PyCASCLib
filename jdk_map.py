JDK_MAP = {
    'windows': {
        8: {
            32: 'https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u312-b07/OpenJDK8U-jdk_x86'
                '-32_windows_hotspot_8u312b07.zip',
            64: 'https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u312-b07/OpenJDK8U'
                '-jdk_x64_windows_hotspot_8u312b07.zip'
        },
        11: {
            32: 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.13%2B8/OpenJDK11U-jdk_x86'
                '-32_windows_hotspot_11.0.13_8.zip',
            64: 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.13%2B8/OpenJDK11U'
                '-jdk_x64_windows_hotspot_11.0.13_8.zip'
        },
        16: {
            32: 'https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x86'
                '-32_windows_hotspot_16.0.2_7.zip',
            64: 'https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U'
                '-jdk_x64_windows_hotspot_16.0.2_7.zip',

        },
        17: {
            32: 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.1%2B12/OpenJDK17U-jdk_x86'
                '-32_windows_hotspot_17.0.1_12.zip',
            64: 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.1%2B12/OpenJDK17U'
                '-jdk_x64_windows_hotspot_17.0.1_12.zip',
        }
    },
    'linux': {
        8: {  # openjdk doesn't have x86 for linux maybe contact the maintainer
            64: 'https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u312-b07/OpenJDK8U'
                '-jdk_x64_linux_hotspot_8u312b07.tar.gz'
        },
        11: {
            64: 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.13%2B8/OpenJDK11U'
                '-jdk_x64_linux_hotspot_11.0.13_8.tar.gz'
        },
        16: {
            64: 'https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U'
                '-jdk_x64_linux_hotspot_16.0.2_7.tar.gz'
        },
        17: {
            64: 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.1%2B12/OpenJDK17U'
                '-jdk_x64_linux_hotspot_17.0.1_12.tar.gz'
        }
    },
    'mac': {
        8: {
            64: 'https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u312-b07/OpenJDK8U'
                '-jdk_x64_mac_hotspot_8u312b07.tar.gz'
        },
        11: {
            64: 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.13%2B8/OpenJDK11U'
                '-jdk_x64_mac_hotspot_11.0.13_8.tar.gz'
        },
        16: {
            64: 'https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U'
                '-jdk_x64_mac_hotspot_16.0.2_7.tar.gz'
        },
        17: {
            64: 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.1%2B12/OpenJDK17U'
                '-jdk_x64_mac_hotspot_17.0.1_12.tar.gz'
        }
    }
}
