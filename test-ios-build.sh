#!/bin/bash

# Test script to verify iOS build configuration fix
# Run this on macOS to verify the fix works

echo "=== iOS Build Configuration Test ==="
echo ""

# Check OS
OS_NAME=$(uname -s)
echo "Operating System: $OS_NAME"
echo ""

if [[ "$OS_NAME" == "Darwin" ]]; then
    echo "✅ Running on macOS - iOS targets should be enabled"
    echo ""

    # Check Java version
    echo "Java version:"
    java -version 2>&1 | head -3
    echo ""

    # Test Gradle configuration
    echo "Testing Gradle configuration..."
    ./gradlew help --no-daemon

    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Gradle configuration successful"
        echo ""

        # Attempt to build iOS framework
        echo "Building iOS framework for simulator..."
        ./gradlew :shared:linkDebugFrameworkIosSimulatorArm64 --no-daemon --stacktrace

        if [ $? -eq 0 ]; then
            FRAMEWORK="shared/build/bin/iosSimulatorArm64/debugFramework/shared.framework"
            if [ -d "$FRAMEWORK" ]; then
                echo ""
                echo "✅ iOS framework built successfully!"
                echo "Location: $FRAMEWORK"
                echo "Size: $(du -sh $FRAMEWORK | cut -f1)"
                echo ""
                echo "Framework contents:"
                ls -lh "$FRAMEWORK/"
            else
                echo "❌ Framework directory not found at expected location"
                exit 1
            fi
        else
            echo "❌ iOS framework build failed"
            exit 1
        fi
    else
        echo "❌ Gradle configuration failed"
        exit 1
    fi
else
    echo "⚠️  Not running on macOS - iOS builds require macOS with Xcode"
    echo "This script is for macOS only. On Windows, use:"
    echo '  $env:JAVA_HOME = "C:\Program Files\Android\Android Studio\jbr"'
    echo '  $env:Path = "$env:JAVA_HOME\bin;$env:Path"'
    echo '  .\gradlew.bat :shared:compileDebugKotlinAndroid --no-daemon'
    exit 0
fi

