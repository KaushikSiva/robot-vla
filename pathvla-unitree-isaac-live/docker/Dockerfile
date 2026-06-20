ARG ISAAC_BASE_IMAGE
FROM ${ISAAC_BASE_IMAGE}

ENV ACCEPT_EULA=Y
ENV PRIVACY_CONSENT=Y
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace/pathvla-unitree-isaac-live

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements-dev.txt

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
