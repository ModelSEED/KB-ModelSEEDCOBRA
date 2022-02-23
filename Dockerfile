FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

RUN apt-get update
RUN apt-get -y install g++ cmake swig

RUN mkdir -p /opt/build
RUN git clone https://github.com/ModelSEED/ModelSEEDpy.git /opt/build/ModelSEEDpy
RUN git clone -b cobra-model https://github.com/Fxe/cobrakbase.git /opt/build/cobrakbase

RUN pip install /opt/build/ModelSEEDpy
RUN pip install /opt/build/cobrakbase

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
