from __future__ import division

import numpy as np

from pgmpy.models import BayesianModel
from pgmpy.factors import LinearGaussianCPD


class LinearGaussianBayesianNetwork(BayesianModel):
    """
    A Linear Gaussain Bayesian Network is a Bayesian Network, all
    of whose variables are continuous, and where all of the CPDs
    are linear Gaussians.

    An important result is that the linear Gaussian Bayesian Networks
    are an alternative representation for the class of multivariate
    Gaussian distributions.

    """
    def __init__(self, ebunch=None):
        super(LinearGaussianBayesianNetwork, self).__init__(ebunch)

        self._jgd = None

    def add_cpds(self, *cpds):
        """
        Add linear Gaussian CPD (Conditional Probability Distribution)
        to the Bayesian Model.

        Parameters
        ----------
        cpds  :  instances of LinearGaussianCPD
            List of LinearGaussianCPDs which will be associated with the model

        Examples
        --------
        >>> from pgmpy.models import LinearGaussianBayesianNetwork
        >>> from pgmpy.factors import LinearGaussianCPD
        >>> model = LinearGaussianBayesianNetwork([('x1', 'x2'), ('x2', 'x3')])
        >>> cpd1 = LinearGaussianCPD('x1', 1, 4)
        >>> cpd2 = LinearGaussianCPD('x2', -5, 4, ['x1'], [0.5])
        >>> cpd3 = LinearGaussianCPD('x3', 4, 3, ['x2'], [-1])
        >>> model.add_cpds(cpd1, cpd2, cpd3)
        >>> for cpd in model.cpds:
                print(cpd)

        P(x1) = N(1; 4)
        P(x2| x1) = N(0.5*x1_mu); -5)
        P(x3| x2) = N(-1*x2_mu); 4)

        """
        for cpd in cpds:
            if not isinstance(cpd, LinearGaussianCPD):
                raise ValueError('Only LinearGaussianCPD can be added.')

            if set(cpd.variables) - set(cpd.variables).intersection(
                    set(self.nodes())):
                raise ValueError('CPD defined on variable not in the model', cpd)

            for prev_cpd_index in range(len(self.cpds)):
                if self.cpds[prev_cpd_index].variable == cpd.variable:
                    logging.warning("Replacing existing CPD for {var}".format(var=cpd.variable))
                    self.cpds[prev_cpd_index] = cpd
                    break
            else:
                self.cpds.append(cpd)

    def get_cpds(self, node=None):
        """
        Returns the cpd of the node. If node is not specified returns all the CPDs
        that have been added till now to the graph

        Parameter
        ---------
        node: any hashable python object (optional)
            The node whose CPD we want. If node not specified returns all the
            CPDs added to the model.

        Returns
        -------
        A list of linear Gaussian CPDs.

        Examples
        --------
        >>> from pgmpy.models import LinearGaussianBayesianNetwork
        >>> form pgmpy.factors import LinearGaussianCPD
        >>> model = LinearGaussianBayesianNetwork([('x1', 'x2'), ('x2', 'x3')])
        >>> cpd1 = LinearGaussianCPD('x1', 1, 4)
        >>> cpd2 = LinearGaussianCPD('x2', -5, 4, ['x1'], [0.5])
        >>> cpd3 = LinearGaussianCPD('x3', 4, 3, ['x2'], [-1])
        >>> model.add_cpds(cpd1, cpd2, cpd3)
        >>> model.get_cpds()
        """
        return super(LinearGaussianBayesianNetwork, self).get_cpds(node)

    def remove_cpds(self, *cpds):
        """
        Removes the cpds that are provided in the argument.

        Parameters
        ----------
        *cpds: LinearGaussianCPD object
            A LinearGaussianCPD object on any subset of the variables
            of the model which is to be associated with the model.

        Examples
        --------
        >>> from pgmpy.models import LinearGaussianBayesianNetwork
        >>> form pgmpy.factors import LinearGaussianCPD
        >>> model = LinearGaussianBayesianNetwork([('x1', 'x2'), ('x2', 'x3')])
        >>> cpd1 = LinearGaussianCPD('x1', 1, 4)
        >>> cpd2 = LinearGaussianCPD('x2', -5, 4, ['x1'], [0.5])
        >>> cpd3 = LinearGaussianCPD('x3', 4, 3, ['x2'], [-1])
        >>> model.add_cpds(cpd1, cpd2, cpd3)
        >>> for cpd in model.get_cpds():
                print(cpd)

        P(x1) = N(1; 4)
        P(x2| x1) = N(0.5*x1_mu); -5)
        P(x3| x2) = N(-1*x2_mu); 4)

        >>> model.remove_cpds(cpd2, cpd3)
        >>> for cpd in model.get_cpds():
                print(cpd)

        P(x1) = N(1; 4)

        """
        return super(LinearGaussianBayesianNetwork, self).remove_cpds(*cpds)
