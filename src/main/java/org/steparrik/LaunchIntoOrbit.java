package org.steparrik;

import krpc.client.Connection;

import krpc.client.RPCException;

import krpc.client.Stream;

import krpc.client.StreamException;

import krpc.client.services.SpaceCenter;

import krpc.client.services.SpaceCenter.Flight;

import krpc.client.services.SpaceCenter.Node;

import krpc.client.services.SpaceCenter.ReferenceFrame;

import krpc.client.services.SpaceCenter.Resources;


import org.javatuples.Triplet;


import java.io.IOException;

import java.lang.Math;


public class LaunchIntoOrbit {

    public static void main(String[] args)

        throws IOException, RPCException, InterruptedException, StreamException {

        Connection connection = Connection.newInstance("Launch into orbit");

        SpaceCenter spaceCenter = SpaceCenter.newInstance(connection);

        SpaceCenter.Vessel vessel = spaceCenter.getActiveVessel();


        float turnStartAltitude = 250;

        float turnEndAltitude = 45000;

        float targetAltitude = 150000;


        // Set up streams for telemetry

        spaceCenter.getUT();

        Stream<Double> ut = connection.addStream(SpaceCenter.class, "getUT");

        ReferenceFrame refFrame = vessel.getSurfaceReferenceFrame();

        Flight flight = vessel.flight(refFrame);

        Stream<Double> altitude = connection.addStream(flight, "getMeanAltitude");

        Stream<Double> apoapsis =

            connection.addStream(vessel.getOrbit(), "getApoapsisAltitude");

        Resources stage2Resources = vessel.resourcesInDecoupleStage(2, false);

        Stream<Float> srbFuel =

            connection.addStream(stage2Resources, "amount", "SolidFuel");


        // Pre-launch setup

        vessel.getControl().setSAS(false);

        vessel.getControl().setRCS(false);

        vessel.getControl().setThrottle(1);


        // Countdown...

        System.out.println("3...");

        Thread.sleep(1000);

        System.out.println("2...");

        Thread.sleep(1000);

        System.out.println("1...");

        Thread.sleep(1000);