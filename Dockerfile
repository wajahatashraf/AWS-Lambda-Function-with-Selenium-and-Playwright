FROM public.ecr.aws/lambda/python:3.12

# ======================================================
# 1. Install system dependencies for Chrome + Playwright
# ======================================================
RUN microdnf install -y \
    unzip xz tar bzip2 gzip \
    alsa-lib atk at-spi2-atk cups-libs \
    libXcomposite libXcursor libXdamage libXext libXi libXrandr \
    libXScrnSaver libXtst libXt pango gtk3 mesa-libgbm \
    nss nss-tools jq \
    && microdnf clean all

# ======================================================
# 2. Install Google Chrome + Chromedriver via your script
# ======================================================
COPY chrome-installer.sh /opt/
RUN chmod +x /opt/chrome-installer.sh && \
    /opt/chrome-installer.sh && \
    rm /opt/chrome-installer.sh

# ======================================================
# 3. Install Python dependencies
# ======================================================
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# ======================================================
# 4. Install Playwright & Chromium (EXACT as your working version)
# ======================================================
RUN pip install --no-cache-dir playwright && \
    mkdir -p ${LAMBDA_TASK_ROOT}/.playwright && \
    PLAYWRIGHT_BROWSERS_PATH=${LAMBDA_TASK_ROOT}/.playwright \
    playwright install chromium

# Let Playwright know where the browser is
ENV PLAYWRIGHT_BROWSERS_PATH=/var/task/.playwright

# ======================================================
# 5. Copy all handler files
# ======================================================
COPY combined_handler.py ${LAMBDA_TASK_ROOT}/
COPY selenium_handler.py ${LAMBDA_TASK_ROOT}/
COPY playwright_handler.py ${LAMBDA_TASK_ROOT}/

# Copy scripts & tests
COPY scripts/ ${LAMBDA_TASK_ROOT}/scripts/
COPY tests/ ${LAMBDA_TASK_ROOT}/tests/

# ======================================================
# 6. Lambda entry point (combined handler)
# ======================================================
CMD ["combined_handler.lambda_handler"]
