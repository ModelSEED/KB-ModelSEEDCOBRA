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

# stupid fix to remove conflict of numpy
RUN rm -rf /miniconda/lib/python3.6/site-packages/numpy*

RUN pip install --upgrade pip
RUN pip install git+https://github.com/ModelSEED/ModelSEEDpy.git@2aa8a21525bb7006b720f423ca43b518a8632252
RUN pip install git+https://github.com/Fxe/cobrakbase.git@76c53a3448e8f86460af285ec87eb98372b8ae2b

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
