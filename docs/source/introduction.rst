Introduction
===================

Electronic Gas Analyzers for Mechanical Ventilators are expensive
($10K or more) and under certain circumstances (like during the
peak of the Covid-19 crisis), difficult to source.

While its cost could not represent a problem for hospitals,
medical schools, and medical engineering companies,
it is a hurdle for small businesses, startups,
and individuals interested in the research and development
of mechanical ventilation.

During COVID-19 crisis this was much needed


The problem
#################

When COVID-19 crisis got heated, the response from
the maker community was overwhelmingly fast and furious.
In particular, to create open-source ventilators.

Soon to realize that testing them for safety was not
an easy or cheap task to do.
Gas analyzer equipment is expensive for a regular maker,
but also, in painful shortage.

Testing mechanical ventilators costs thousand of dollars!

A possible (hardware) solution
##############################

As a cost-effective alternative, it is possible to build an
operational tester for the development of experimental mechanical
ventilators using an Arduino Board and pressure and airflow sensors.

Using an opensource design, the Venmont, I built a derivative working system
that includes several improvements to the original design.

While the system used as a base already includes a minimal
graphical interface and means to record the results,
it lacks basic features like for instance, the capability
to uniquely identify different test sessions
(i.e. the output is recorded as a single, infinite time series,
regardless of the device being tested).

Also, the data is stored in a proprietary repository on the cloud,
owned by VentMont, making it nonviable for storing sensitive information.
