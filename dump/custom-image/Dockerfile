ARG BASE_IMAGE=quay.io/modh/odh-generic-data-science-notebook:v2-2023a-20230322
# hadolint ignore=DL3006
FROM ${BASE_IMAGE}

USER 0

# hadolint ignore=DL3003
RUN cd /opt/app-root/bin \
 && micropipenv install \
 && rm -f Pipfile.lock \
 && chmod -R g+w /opt/app-root/lib/python3.9/site-packages \
 && fix-permissions /opt/app-root -P

 USER 1001
